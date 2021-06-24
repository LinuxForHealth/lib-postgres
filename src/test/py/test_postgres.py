from whpa_cdp_postgres import postgres
import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test(mocker):

    config = {
        'username': 'none',
        'password': 'empty',
        'hostport': '',
        'database': ''
    }
    query = 'select * from distributors'
    db = postgres.Postgres('test',config)
    db.initialized = True
    mocker.patch.object(db, "pool")
    connection = AsyncMock()
    db.pool.acquire().__aenter__.return_value = connection
    connection.execute = AsyncMock()
    connection.execute.return_value = 3
    result = await db.execute(query)
    connection.execute.assert_called_with(query)
    assert result == 3

    # result = await db.fetch('select * from distributors')
    # print(result)

    # @db.query("select * from distributors")
    # async def test_query(): pass

    # @db.query("select * from distributors", call='fetch')
    # async def test_fetch_query(): pass

    # print(await test_query())
    # print(await test_fetch_query())

    #     HL7BatchTrackingDao.insert_new_batch.assert_called_once()
    # HL7BatchTrackingDao.update_hl7batch_with_storage_id.assert_called_once()
    # mock_minio_upload.assert_called_once()
    # mock_kafka_call.assert_called_once()

