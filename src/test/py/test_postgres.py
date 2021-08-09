import asyncio
import logging
from unittest import mock

from whpa_cdp_postgres import postgres
import pytest
from unittest.mock import AsyncMock, Mock, MagicMock
from whpa_cdp_postgres import config

#initialize a Postgres object for tests that require one.
configuration = config.PostgresLibSettings (
    username = 'none',
    password = 'empty',
    hostport = 'somewhere:8443',
    database = 'thedatabase'
)


@pytest.mark.asyncio
@mock.patch('whpa_cdp_postgres.postgres.Postgres', autospec=True)
async def test_factory_constructs_and_initializes(postgres_constructor):
    mock_config = MagicMock()
    name = "some name"
    returned_object = await postgres.create_postgres_pool(postgres_config=mock_config, name=name)
    postgres_constructor.assert_called_once_with(postgres_config=mock_config, name=name)
    #Verify the object has been initialized
    returned_object.initialize_connection.assert_called_once_with()

@pytest.mark.asyncio
@mock.patch('whpa_cdp_postgres.postgres.config.PostgresLibSettings', autospec=True)
@mock.patch('whpa_cdp_postgres.postgres.Postgres', autospec=True)
async def test_factory_constructs_and_initializes_with_new_config_if_none(postgres_constructor, postgres_lib_config):
    name = "some name"
    returned_object = await postgres.create_postgres_pool(name=name)
    postgres_lib_config.assert_called_once_with()
    postgres_constructor.assert_called_once_with(postgres_config=postgres_lib_config.return_value, name=name)
    #Verify the object has been initialized
    returned_object.initialize_connection.assert_called_once_with()

@pytest.mark.asyncio
@mock.patch('whpa_cdp_postgres.postgres.asyncpg', autospec=True)
async def test_factory_invokes(mock_asyncpg):
    test_object=postgres.Postgres(name='test',postgres_config=configuration)
    logging.error("test obj " + str(test_object))
    #mock the async create pool
    create_pool = AsyncMock()
    mock_asyncpg.create_pool = create_pool
    await test_object.initialize_connection()
    #note: dns is solely based on configs
    create_pool.assert_called_once_with(dsn="postgresql://none:empty@somewhere:8443/thedatabase", command_timeout=60)
    assert test_object.pool == create_pool.return_value
    assert test_object.initialized is True

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

