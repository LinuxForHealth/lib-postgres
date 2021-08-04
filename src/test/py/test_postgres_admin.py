from whpa_cdp_postgres import postgres
from whpa_cdp_postgres import postgres_admin

import pytest


# initialize a Postgres object for tests that require one.
config = {"username": "none", "password": "empty", "hostport": "", "database": ""}
db = postgres.Postgres("test", config)
db.initialized = True

PA = postgres_admin.PostgresAdmin(db)


def test_create_statement_list_from_sql_block():
    """Verifies the create_statement_list_from_sql_block() method functionality"""

    sql_text = ""
    with open("./src/test/data/test_sql_block.sql", "r") as sql_text_file:
        sql_text = sql_text_file.read()

    expected_statement_1 = ""
    with open(
        "./src/test/data/expected_sql_stmt_1.sql", "r"
    ) as expected_sql_text_file_1:
        expected_statement_1 = expected_sql_text_file_1.read()

    expected_statement_2 = ""
    with open(
        "./src/test/data/expected_sql_stmt_2.sql", "r"
    ) as expected_sql_text_file_2:
        expected_statement_2 = expected_sql_text_file_2.read()

    statements = PA.create_statement_list_from_sql_block(sql_text)

    assert statements[0] == expected_statement_1
    assert statements[1] == expected_statement_2


@pytest.mark.asyncio
async def test_execute_sql_block_throws_on_unexpected_exception():
    """Verify we throw an exception on failures."""
    with pytest.raises(Exception):
        await PA.execute_sql_block("some sql that won't work")
