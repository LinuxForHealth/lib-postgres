import os

from pydantic import ValidationError
from whpa_cdp_postgres import config as configuration
import pytest
from unittest.mock import AsyncMock, Mock
from caf_logger import logger as caflogger
import importlib

logger = caflogger.get_logger('whpa_cdp_postgres.test_config')

#test defaults and basic loading
#test env override
#test
@pytest.fixture(autouse=True)
def reset():
    reset_env_vars()

def reset_env_vars():
    for env_var in ("WHPA_CDP_POSTGRES_CONFIG_FILE", "WHPA_CDP_POSTGRES_SECRETS", "POSTGRES_LIB_USERNAME", "POSTGRES_LIB_PASSWORD", "POSTGRES_LIB_HOSTPORT", "POSTGRES_LIB_DATABASE", "PoStGrEs_lIb_uSeRnAmE", "PoStGrEs_lIb_pAsSwOrD", "PoStGrEs_lIb_hOsTpOrT", "PoStGrEs_lIb_dAtAbAsE",):
        if env_var in os.environ:
            del os.environ[env_var]

def test_defaults_and_that_bad_file_is_not_an_error():
    #TODO: consider that defaults are a bad idea and split this test to an error if nothing is given for a specific, a test that env + no secret is fine and secret + no env is fine
    os.environ["WHPA_CDP_POSTGRES_CONFIG_FILE"]="non-existent.env"
    os.environ["WHPA_CDP_POSTGRES_SECRETS"]="non-existent/secrets"
    test_object = configuration.PostgresLibSettings()

    assert test_object is not None
    logger.warn(("BEHOLD", str(test_object)))
    expected = configuration.PostgresLibSettings(
        username = 'postgres',
        password = "",
        hostport = "localhost:5432",
        database = "defaultdb",

    )
    assert expected == test_object

def test_defaults_and_that_none_file_is_not_an_error():
    test_object = configuration.PostgresLibSettings()

    assert test_object is not None
    logger.warn(("BEHOLD", str(test_object)))
    test_object = configuration.PostgresLibSettings(_env_file=None, _secrets_dir=None)  #This is the only way to set this.  Setting an env variable to None is not possible (as env vars are strings) and empty string just means that it uses the default name
    expected = configuration.PostgresLibSettings(
        username = 'postgres',
        password = "",
        hostport = "localhost:5432",
        database = "defaultdb",

    )
    assert expected == test_object

def test_env_var_override_succeeds():
    os.environ["POSTGRES_LIB_USERNAME"]="overridden_username"
    os.environ["POSTGRES_LIB_PASSWORD"]="overridden_password"
    os.environ["POSTGRES_LIB_HOSTPORT"]="overridden_hostport"
    os.environ["POSTGRES_LIB_DATABASE"]="overridden_database"
    test_object = configuration.PostgresLibSettings()

    assert test_object is not None
    logger.warn(("BEHOLD", str(test_object)))
    assert test_object.username == 'overridden_username'

def test_field_override():
    #note: if this one is broken, it makes the other tests harder to do
    test_object = configuration.PostgresLibSettings(
        username='test_username',
        password='test_password',
        hostport='test_hostport',
        database='test_database',
    )

    assert test_object is not None
    logger.warn(("BEHOLD", str(test_object)))
    assert test_object.username == 'test_username'
    assert test_object.password == 'test_password'
    assert test_object.hostport == 'test_hostport'
    assert test_object.database == 'test_database'

# def test_env_var_filenames():
#     os.environ["WHPA_CDP_POSTGRES_CONFIG_FILE"]="overridden_file"
#     test_object = configuration.PostgresLibSettings()
#
#     assert test_object is not None
#     logger.warn(("BEHOLD", str(test_object)))
#     assert test_object.username == 'something to fail so I see warnings'
#
# def mock_files(secret_dir)
#     def flexible_side_effect(file_name):
#         if file_name in file_map:
#             return file_map[file_name]
#         else:
#             global g__test_utils__original_open
#             return g__test_utils__original_open(file_name)
#
#     global g__test_utils__original_open
#     return_value = MagicMock(name='open', spec=g__test_utils__original_open)
#     return_value.side_effect = flexible_side_effect
#     return return_value


#test default filenames work
    #may need fancy mocking.  This seems not doable

def test_env_var_override_all_secrets():

    os.environ["WHPA_CDP_POSTGRES_CONFIG_FILE"]="src/test/resources/empty_postgres.env"
    os.environ["WHPA_CDP_POSTGRES_SECRETS"]="src/test/resources/full_secrets"

    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings()
    expected = configuration.PostgresLibSettings(
        username='testsecretusername',
        password='testsecretpassword',
        hostport='testsecrethostport',
        database='testsecretdatabase',
    )

    assert test_object == expected

def test_filename_override_all_secrets():

    os.environ["WHPA_CDP_POSTGRES_CONFIG_FILE"]="src/test/resources/empty_postgres.env"

    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings(_secrets_dir='src/test/resources/full_secrets')
    expected = configuration.PostgresLibSettings(
        username='testsecretusername',
        password='testsecretpassword',
        hostport='testsecrethostport',
        database='testsecretdatabase',
    )

    assert test_object == expected


def test_env_var_override_all_envfile():

    os.environ["WHPA_CDP_POSTGRES_CONFIG_FILE"]="src/test/resources/full_postgres.env"
    os.environ["WHPA_CDP_POSTGRES_SECRETS"]="src/test/resources/empty_secrets"

    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings()
    expected = configuration.PostgresLibSettings(
        username='testenvusername',
        password='testenvpassword',
        hostport='testenvhostport',
        database='testenvdatabase',
    )

    assert test_object == expected

def test_filename_override_all_envfile():

    os.environ["WHPA_CDP_POSTGRES_SECRETS"]="src/test/resources/empty_secrets"

    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings(_env_file='src/test/resources/full_postgres.env')
    expected = configuration.PostgresLibSettings(
        username='testenvusername',
        password='testenvpassword',
        hostport='testenvhostport',
        database='testenvdatabase',
    )

    assert test_object == expected

def test_env_var_override_envfile_takes_priority_over_secret():

    os.environ["WHPA_CDP_POSTGRES_CONFIG_FILE"]="src/test/resources/full_postgres.env"
    os.environ["WHPA_CDP_POSTGRES_SECRETS"]="src/test/resources/full_secrets"

    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings()
    expected = configuration.PostgresLibSettings(
        username='testenvusername',
        password='testenvpassword',
        hostport='testenvhostport',
        database='testenvdatabase',
    )

    assert test_object == expected

def test_filename_override_envfile_takes_priority_over_secret():


    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings(_env_file='src/test/resources/full_postgres.env', _secrets_dir="src/test/resources/full_secrets")
    expected = configuration.PostgresLibSettings(
        username='testenvusername',
        password='testenvpassword',
        hostport='testenvhostport',
        database='testenvdatabase',
    )

    assert test_object == expected


def test_env_var_override_env_var_takes_priority_over_env_file():

    os.environ["POSTGRES_LIB_USERNAME"] = "testenvvarusername"
    os.environ["POSTGRES_LIB_PASSWORD"] = "testenvvarpassword"
    os.environ["POSTGRES_LIB_HOSTPORT"] = "testenvvarhostport"
    os.environ["POSTGRES_LIB_DATABASE"] = "testenvvardatabase"

    os.environ["WHPA_CDP_POSTGRES_CONFIG_FILE"]="src/test/resources/full_postgres.env"

    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings(_secrets_dir=None)
    expected = configuration.PostgresLibSettings(
        username='testenvvarusername',
        password='testenvvarpassword',
        hostport='testenvvarhostport',
        database='testenvvardatabase',
    )

    assert test_object == expected

def test_filename_override_env_var_takes_priority_over_env_file():

    os.environ["POSTGRES_LIB_USERNAME"] = "testenvvarusername"
    os.environ["POSTGRES_LIB_PASSWORD"] = "testenvvarpassword"
    os.environ["POSTGRES_LIB_HOSTPORT"] = "testenvvarhostport"
    os.environ["POSTGRES_LIB_DATABASE"] = "testenvvardatabase"

    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings(_env_file='src/test/resources/full_postgres.env', _secrets_dir=None)
    expected = configuration.PostgresLibSettings(
        username='testenvvarusername',
        password='testenvvarpassword',
        hostport='testenvvarhostport',
        database='testenvvardatabase',
    )

    assert test_object == expected


def test_input_param_takes_priority_over_env_var():

    os.environ["POSTGRES_LIB_USERNAME"] = "testenvvarusername"
    os.environ["POSTGRES_LIB_PASSWORD"] = "testenvvarpassword"
    os.environ["POSTGRES_LIB_HOSTPORT"] = "testenvvarhostport"
    os.environ["POSTGRES_LIB_DATABASE"] = "testenvvardatabase"



    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings(
        username='testinputparamusername',
        password='testinputparampassword',
        hostport='testinputparamhostport',
        database='testinputparamdatabase',
    )

    reset_env_vars()

    expected = configuration.PostgresLibSettings(
        username='testinputparamusername',
        password='testinputparampassword',
        hostport='testinputparamhostport',
        database='testinputparamdatabase',
    )

    assert test_object == expected

    #also check each individually, in case the test setup becomes subtly invalid
    assert test_object.username == 'testinputparamusername'
    assert test_object.password == 'testinputparampassword'
    assert test_object.hostport == 'testinputparamhostport'
    assert test_object.database == 'testinputparamdatabase'

def test_input_param_is_case_sensitive():

    importlib.reload(configuration)

    with pytest.raises(ValidationError):
        test_object = configuration.PostgresLibSettings(
            UsErNaMe='tEsTiNpUtPaRaMUsErNaMe',
            PaSsWoRd='tEsTiNpUtPaRaMPaSsWoRd',
            HoStNaMe='tEsTiNpUtPaRaMHoStNaMe',
            DaTaBaSe='tEsTiNpUtPaRaMDaTaBaSe',
        )


def test_env_var_is_not_case_sensitive_in_keys():

    os.environ["PoStGrEs_lIb_uSeRnAmE"] = "TeStEnVvAruSeRnAmE"
    os.environ["PoStGrEs_lIb_pAsSwOrD"] = "TeStEnVvArpAsSwOrD"
    os.environ["PoStGrEs_lIb_hOsTpOrT"] = "TeStEnVvArhOsTpOrT"
    os.environ["PoStGrEs_lIb_dAtAbAsE"] = "TeStEnVvArdAtAbAsE"



    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings()

    reset_env_vars()

    expected = configuration.PostgresLibSettings(
        username='TeStEnVvAruSeRnAmE',
        password='TeStEnVvArpAsSwOrD',
        hostport='TeStEnVvArhOsTpOrT',
        database='TeStEnVvArdAtAbAsE',
    )

    assert test_object == expected

    # It should still have case sensitive values
    unexpected = configuration.PostgresLibSettings(
        username='testenvvarusername',
        password='testenvvarpassword',
        hostport='testenvvarhostport',
        database='testenvvardatabase',
    )

    assert test_object != unexpected

def test_env_file_is_not_case_sensitive_in_keys():

    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings(_env_file='src/test/resources/mixed_case_postgres.env', _secrets_dir=None)

    reset_env_vars()

    expected = configuration.PostgresLibSettings(
        username='tEsTeNvUsErNaMe',
        password='tEsTeNvPaSsWoRd',
        hostport='tEsTeNvHoStPoRt',
        database='tEsTeNvDaTaBaSe',
    )

    assert test_object == expected

    # It should still have case sensitive values
    unexpected = configuration.PostgresLibSettings(
        username='testenvusername',
        password='testenvpassword',
        hostport='testenvhostport',
        database='testenvdatabase',
    )

    assert test_object != unexpected

def test_secret_file_is_not_case_sensitive_in_keys():

    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings(_env_file=None, _secrets_dir='src/test/resources/mixed_case_secrets')

    reset_env_vars()

    expected = configuration.PostgresLibSettings(
        username='TeStSeCrEtUsErNaMe',
        password='TeStSeCrEtPaSsWoRd',
        hostport='TeStSeCrEtHoStPoRt',
        database='TeStSeCrEtDaTaBaSe',
    )

    assert test_object == expected

    # It should still have case sensitive values
    unexpected = configuration.PostgresLibSettings(
        username='testsecretusername',
        password='testsecretpassword',
        hostport='testsecrethostport',
        database='testsecretdatabase',
    )

    assert test_object != unexpected

def test_mixed_values():
    os.environ["POSTGRES_LIB_HOSTPORT"] = "testenvvarhostport"

    importlib.reload(configuration)
    test_object = configuration.PostgresLibSettings(_env_file='src/test/resources/single_username_postgres.env', _secrets_dir='src/test/resources/single_password_secrets', database='testinitdatabase')

    reset_env_vars()

    expected = configuration.PostgresLibSettings(
        username='testenvusername',
        password='testsecretpassword',
        hostport='testenvvarhostport',
        database='testinitdatabase',
    )

    assert test_object == expected