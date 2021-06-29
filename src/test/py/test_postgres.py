from whpa_cdp_postgres import postgres
import pytest
from unittest.mock import AsyncMock, Mock

#initialize a Postgres object for tests that require one.
config = {
    'username': 'none',
    'password': 'empty',
    'hostport': '',
    'database': ''
}
db = postgres.Postgres('test',config)
db.initialized = True


@pytest.mark.asyncio
async def test_execute(mocker):

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
    db.name = 'name'
    result = db.get_name()
    assert result == 'name'

