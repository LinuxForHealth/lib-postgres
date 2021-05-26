from whpa_cdp_postgres import postgres
import asyncio
import asynctest
from asynctest import CoroutineMock, MagicMock, patch

async def test():

    db = await postgres.create_postgres_pool()
    result = await db.execute('select * from distributors')
    print(result)

    result = await db.fetch('select * from distributors')
    print(result)

    @db.query("select * from distributors")
    async def test_query(): pass

    @db.query("select * from distributors", call='fetch')
    async def test_fetch_query(): pass

    print(await test_query())
    print(await test_fetch_query())




class PatientLookupDaoTest(asynctest.TestCase):
    async def test_patient_lookup(self):
        '''
        mock_pool = MagicMock(name='asyncpg')
        with patch('asyncpg.create_pool', new=mock_pool):
            pool = MagicMock(name="pool")
            conn = CoroutineMock(name="conn")
            mock_pool().__aenter__.return_value = pool
            pool.acquire().__aenter__.return_value = conn
            conn.fetch = CoroutineMock()
            conn.fetch.return_value = 5
            result = await patient_lookup_dao.patient_lookup(None)
        
        self.assertEqual(result, 5)
        '''
        pass

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(test())