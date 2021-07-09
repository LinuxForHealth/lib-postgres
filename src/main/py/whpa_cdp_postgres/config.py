import os

from whi_caf_lib_configreader import config as configreader
from caf_logger import logger as caflogger
from . import logging_codes

DEFAULT_CONFIG_HEADER = 'Postgres'
REQUIRED_CONFIG_KEYS= [
    'username',
    'password',
    'hostport',
    'database'
]


logger = caflogger.get_logger('whpa_cdp_postgres.config')

postgres_config_path = os.getenv('WHPA_CDP_POSTGRES_CONFIG_FILE', default='/var/app/config/postgres.ini')
postgres_secrets = os.getenv('WHPA_CDP_POSTGRES_SECRETS', default='/var/app/config/secrets')

config = None

def load_config():
    global config
    logger.info(logging_codes.LOADING_CONFIG, postgres_config_path, postgres_secrets)
    config = configreader.load_config(postgres_config_path, postgres_secrets)

def get_config_section(section_name):
    if config is not None:
        configreader.validate_config(config, section_name, REQUIRED_CONFIG_KEYS)
        return configreader.get_section(config, section_name)
    else:
        logger.error(logging_codes.CONFIG_ACCESSED_BEFORE_LOADING)
        raise ValueError('configuration not initialized')
