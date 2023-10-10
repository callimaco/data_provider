from polygon.polygon import Tickers
from ...core.base import TaskArray
from scriba.scriba.scriba import DbManager
from ...core.base import Task, Provider
from ...core.abstract import ProcessPipeLine,
import mysql.connector
from secret.secret_man.secret_man import SecretManager as sm
from concurrent.futures import ThreadPoolExecutor
import asyncio




class Producer:

    def __init__(self, task : Task, buffer: asyncio.Queue) -> None:
        self.task = task.new_push() # deve generare un task di ritorno il metodo tipo create task 
    
    async def sboret(self):
        while True:    
            self.res = await self.task
            await buffer.put(self.res)   

class Consumer:

    ooo = mysql.connector.pooling.MySQLConnectionPool(pool_name='hy', pool_size=5, **sm.config())

    loop = asyncio.get_event_loop()

    db = DbManager(db='finace', table='aaau')

    async def _write_in_db(cls, buffer: asyncio.Queue):

        with ThreadPoolExecutor() as w:
            await cls.loop.run_in_executor(w,cls.db.write, cls.ooo.get_connection())
    
    async def aggiorna_task_con_next_URL_tipo():
        pass

    async def dd(cls, buffer):
        while True:
            item = await buffer.get()
            task_n = asyncio.create_task(cls._write_in_db(buffer=buffer))

buffer = asyncio.Queue()

def main():
    Producer(Tickers(ticker='aaau').get_data(), buffer=buffer)
    Consumer.dd(buffer=buffer)

asyncio.run(main)