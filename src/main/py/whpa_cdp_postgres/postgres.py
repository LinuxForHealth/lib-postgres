import asyncpg
from contextlib import asynccontextmanager
import uuid
import functools

from . import config
from whpa_cdp_postgres import logging_codes
from caf_logger import logger as caflogger

logger = caflogger.get_logger(__name__)


async def create_postgres_pool(config_section=None, name=None):
    if config_section is None:
        config_section = 'Postgres'
    if name is None:
        name = config_section


async def create_postgres_pool(postgres_config=None, name=None):
    if postgres_config is None:
        postgres_config = config.PostgresLibSettings()
    postgres = Postgres(name, postgres_config)
    await postgres.initialize_connection()
    return postgres


class Postgres:
    def __init__(self, name, postgres_config):
        self.pool = None
        self.name = name
        username = postgres_config.username
        password = postgres_config.password
        hostport = postgres_config.hostport
        database = postgres_config.database
        self.dsn = f"postgresql://{username}:{password}@{hostport}/{database}"
        self.initialized = False

    def get_name(self):
        return self.name

    async def initialize_connection(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn, command_timeout=60)
        self.initialized = True

    @asynccontextmanager
    async def acquire(self):
        async with self.pool.acquire() as conn:
            yield conn

    async def execute(self, sql_query, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(sql_query, *args)

    async def execute_in_transaction(self, sql_statements):
        """Execute a list of sql statements in a transaction."""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for stmt in sql_statements:
                    try:
                        await conn.execute(stmt)
                    except Exception as e:
                        logger.error(
                            logging_codes.ERROR_EXECUTING_SQL, str(e), stmt, exc_info=e,
                        )
                        raise

    async def fetch(self, sql_query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(sql_query, *args)

    def query(self, sql_query, call="execute"):
        """Decorator function. Example use cases:
        # Define
        postgres = create_postgres_pool(...)
        @postgres.execute("select * from keyspace.table")
        def select_from_table(): pass

        @postgres.query("select * from table where ID=? and UID=?")
        def select_from_table_where_id(id, uid): pass

        # Usage:
        select_from_table()
        select_from_table_where_id(123, "abcd")
        """

        def decorator_query(func):
            @functools.wraps(func)
            async def wrapper(*args):
                async with self.pool.acquire() as conn:
                    if hasattr(conn, call):
                        db_call = getattr(conn, call)
                        return await db_call(sql_query, *args)
                    else:
                        raise ValueError(f"connection object has no db method {call}")

            return wrapper

        return decorator_query
