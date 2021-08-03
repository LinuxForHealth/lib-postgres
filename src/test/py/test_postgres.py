from whpa_cdp_postgres import postgres
import pytest
from unittest.mock import AsyncMock, Mock
from caf_logger import logger as caflogger

from whpa_cdp_postgres import config

logger = caflogger.get_logger('whpa_cdp_postgres.test_postgres')
#initialize a Postgres object for tests that require one.
configuration = config.PostgresLibSettings (
    username = 'none',
    password = 'empty',
    hostport = 'somewhere:8443',
    database = 'thedatabase'
)



"postgresql://none:empty@somewhere:8443/thedatabase"
@pytest.mark.asyncio
async def test_execute(mocker):
    db = postgres.Postgres(name='test',postgres_config=configuration)
    db.initialized = True
    query = 'SELECT * from distributors'
    mocker.patch.object(db, "pool")
    connection = AsyncMock()
    db.pool.acquire().__aenter__.return_value = connection
    connection.execute = AsyncMock()
    connection.execute.return_value = 3
    result = await db.execute(query)
    connection.execute.assert_called_with(query)
    assert result == 3


@pytest.mark.asyncio
async def test_execute(mocker):
    db = postgres.Postgres(name='test',postgres_config=configuration)
    db.initialized = True
    query = 'SELECT * from distributors'
    mocker.patch.object(db, "pool")
    connection = AsyncMock()
    db.pool.acquire().__aenter__.return_value = connection
    connection.execute = AsyncMock()
    connection.execute.return_value = 3
    result = await db.execute(query)
    connection.execute.assert_called_with(query)
    assert result == 3

@pytest.mark.asyncio
async def test_fetch(mocker):
    db = postgres.Postgres(name='test',postgres_config=configuration)
    db.initialized = True
    query = 'UPDATE distributors SET id=0'
    mocker.patch.object(db, "pool")
    connection = AsyncMock()
    db.pool.acquire().__aenter__.return_value = connection
    connection.fetch = AsyncMock()
    connection.fetch.return_value = 3
    result = await db.fetch(query)
    connection.fetch.assert_called_with(query)
    assert result == 3

def test_get_name():
    db = postgres.Postgres(name='test',postgres_config=configuration)
    db.initialized = True
    db.name = 'name'
    result = db.get_name()
    assert result == 'name'

