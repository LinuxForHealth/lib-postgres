import asyncpg
import re

from whpa_cdp_postgres import postgres
from whpa_cdp_postgres import logging_codes

from caf_logger import logger as caflogger

logger = caflogger.get_logger(__name__)


class PostgresAdmin:
    """Class to encapsulate administrative methods of postgres. These are mostly methods used to manage schemas"""

    SCHEMA_VERSION_COLUMN_NAME = "version"
    SCHEMA_VERSION_TABLE_NAME = "schema_version"

    def __init__(self, postgres_access):
        self._postgres_access = postgres_access

    async def create_schema_version_table(self, schema_name):
        """Create the schema_version_table. This removes the responsibilty of maintaining the schema_version table
        from users and promotes uniformity."""

        # Here lies the current definition of the schema version table.
        # Changes to this schema should be carefully considered.
        sql = f"CREATE TABLE IF NOT EXISTS {schema_name}.{PostgresAdmin.SCHEMA_VERSION_TABLE_NAME} (\
            {PostgresAdmin.SCHEMA_VERSION_COLUMN_NAME} TEXT NOT NULL,\
            created_on TIMESTAMP DEFAULT current_timestamp NOT NULL)"

        await self._postgres_access.execute(sql)

    async def get_schema_version(self, schema_name):
        """Get the current version of the specified schema based on the created date.
        Assumes schema is using our standard schema versioning table."""

        sql = f"SELECT {PostgresAdmin.SCHEMA_VERSION_COLUMN_NAME} FROM {schema_name}.{PostgresAdmin.SCHEMA_VERSION_TABLE_NAME} \
            order by created_on desc limit 1"
        version = 0

        try:
            result = await self._postgres_access.fetch(sql)
            version = result[0][PostgresAdmin.SCHEMA_VERSION_COLUMN_NAME]
        except asyncpg.exceptions.UndefinedTableError:
            logger.warn(
                logging_codes.TABLE_NOT_FOUND,
                f"{schema_name}.{PostgresAdmin.SCHEMA_VERSION_TABLE_NAME}",
            )

        return version

    def create_statement_list_from_sql_block(self, sql_txt):
        """Parse a block of sql text (likely from a file) into idividually executable SQL statements.
        NOTE: This code isn't the most intelligent and likely doesn't handle all cornercases. For sure
        it doesn't support block comments or inline comments across multiline statements. It's assumed
        that sql files processed through this code will be tested. This method should not be used to
        run adhoc queries that haven't been previously verified as parsable. If we need better
        functionality, we should use an actual SQL parser such as sqlparse."""

        stmts = sql_txt.split(r";")
        # Postgres supports using `$$` to quote a value containing characters being escaped.
        in_escaped_string = False

        statement_list = []
        for i in stmts:
            if i.count("$$") % 2 != 0:
                if in_escaped_string:
                    # Add semicolon between substatements.
                    stmt += ";"
                    # Found the ending `$$`, set the flag to be false.
                    # so that the statement can be executed.
                    in_escaped_string = False
                    stmt += i
                else:
                    # Found the starting `$$`, set the flag to be true.
                    # will concatenate the strings until the ending `$$` is found.
                    in_escaped_string = True
                    stmt = i
            else:
                if in_escaped_string:
                    # In the middle of the escaped string, concatenate the string
                    # Add semicolon between substatements
                    stmt += ";"
                    stmt += i
                else:
                    # Not in the middle of the escaped string, this is a complete statement string.
                    stmt = i

            if in_escaped_string:
                continue

            # Remove comments and blank lines. Helps avoid having to code around corner cases.
            cleaned_stmt = ""
            for line in stmt.splitlines(True):
                if line.strip()[0:2] == "--":  # Detect comments
                    continue
                elif line.strip() == "":  # Detect empty lines
                    continue
                else:
                    cleaned_stmt += line

            if cleaned_stmt != "":
                statement_list.append(cleaned_stmt)

        return statement_list

    async def execute_sql_block(self, sql_txt):
        """Execute SQL statements from text block sql_txt in a transaction. These blocks are usually from a SQL file.
        This method parses the SQL and executes each statement within a transaction. Note that "CREATE DATABASE" statements
        cannot be executed in transactions and are filtered out and run outside the transaction."""

        statement_list = self.create_statement_list_from_sql_block(sql_txt)

        # Create database cannot be transactional, so run it separately
        regexp = re.compile(r"create\s+database")
        for stmt in statement_list:
            if regexp.search(stmt.lower()):
                try:
                    await self._postgres_access.execute(stmt)
                # There's no, "IF NOT EXIST" for database creation. Handle it in the code.
                except (asyncpg.exceptions.DuplicateDatabaseError):
                    logger.info(logging_codes.DATABASE_EXISTS)
                except Exception as e:
                    logger.error(
                        logging_codes.ERROR_EXECUTING_SQL, str(e), stmt, exc_info=e
                    )
                    raise

                statement_list.remove(stmt)
                break

        # Run all other statements in a transaction
        await self._postgres_access.execute_in_transaction(statement_list)

    async def insert_schema_version(
        self, schema_name, version, create_schema_table=True
    ):
        """Insert a version number into the schema version table"""

        sql = f"INSERT INTO {schema_name}.{PostgresAdmin.SCHEMA_VERSION_TABLE_NAME} \
            ({PostgresAdmin.SCHEMA_VERSION_COLUMN_NAME}) VALUES ($1)"

        try:
            await self._postgres_access.execute(sql, str(version))
        except asyncpg.exceptions.UndefinedTableError:
            logger.warn(
                logging_codes.TABLE_NOT_FOUND,
                f"{schema_name}.{PostgresAdmin.SCHEMA_VERSION_TABLE_NAME}",
            )

            if create_schema_table:
                logger.info(logging_codes.CREATING_SCHEMA_VERSION_TABLE, schema_name)
                await self.create_schema_version_table(schema_name)
                # Try it again!
                await self.insert_schema_version(
                    schema_name, version, create_schema_table=False
                )

