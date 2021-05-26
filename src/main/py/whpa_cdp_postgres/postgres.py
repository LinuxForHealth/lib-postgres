import asyncpg
from contextlib import asynccontextmanager
import uuid
import functools

from . import config

async def create_postgres_pool(config_section=None, name=None):
    if config_section is None:
        config_section = 'Postgres'
    if name is None:
        name = config_section

    config.load_config()
    postgres_config = config.get_config_section(config_section)
    postgres = Postgres(name, postgres_config)
    await postgres.initialize_connection()
    return postgres


class Postgres():
    def __init__(self, name, postgres_config):
        self.pool = None
        self.name = name
        username = postgres_config['username']
        password = postgres_config['password']
        hostport = postgres_config['hostport']
        database = postgres_config['database']
        self.dsn = f'postgresql://{username}:{password}@{hostport}/{database}'
        self.initialized = False
        
    def get_name(self):
        return self.name

    async def initialize_connection(self):
        self.pool = await asyncpg.create_pool(
            dsn=self.dsn, command_timeout=60
        )
        self.initialized = True

    @asynccontextmanager
    async def acquire(self):
        async with self.pool.acquire() as conn:
            yield conn

    async def execute(self, sql_query, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(sql_query, *args)

    async def fetch(self, sql_query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(sql_query, *args)
            
    def query(self, sql_query, call='execute'):
        """ Example use cases:
            postgres = create_postgres_pool(...)
            @postgres.execute("select * from keyspace.table")
            def select_from_table(): pass
            @cass_driver.query("select * from table where ID=? and UID=?")
            def select_from_table_where_id(id, uid): pass
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
                        raise ValueError(f'connection object has no db method {call}')
            return wrapper
        return decorator_query
