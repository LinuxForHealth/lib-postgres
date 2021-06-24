from whpa_cdp_postgres import postgres
import pytest
import asyncio
import asynctest
from asynctest import CoroutineMock, MagicMock, patch

@pytest.mark.asyncio
async def test(mocker):

    config = {
        'username': 'none',
        'password': 'empty',
        'hostport': '',
        'database': ''
    }
    db = postgres.Postgres('test',config)
    db.initialized = True
    mocker.patch.object(db, "pool")
    print("START")
    print('pool='+db.pool)
    result = await db.execute('select * from distributors')
    print(result)

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

