from typing import List, Dict, Callable, Any
from abc import ABC, abstractclassmethod, abstractmethod
import multiprocessing.queues as mlp_que
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import websockets
import json
import asyncio
from asyncio.queues import Queue

class Loop:
    """A Loop over an iterable"""
        
    def __init__(self) -> None:
        self.loop : List[object] = []
        self._current_index = 0

    def __iter__(self):
        return self

    def __next__(self):

        if not self.loop:
            raise StopIteration

        item = self.loop[self._current_index]
        self.current_indx = (self._current_index + 1) % len(self.task_stack)
        return item

class Http:
    
    @classmethod
    async def _ama(cls):
        async with aiohttp.ClientSession() as ses:
            cls.ses = ses
            await asyncio.sleep(24*60*60)
            pass

    protocol = ('http', 'https', 'wss')
    
    _isinstance = 0
    
    def __init__(self) -> None:
        self._isinstance += 1
        self.auth : Dict[str,str]
        
    async def req(self,query : str, params : Dict[str,str]):


            await self.ses.get(url=query, **params)
        
class Wss:
    _instances = 0
    async def listen(self, url: str, queue: asyncio.Queue) -> None:
        async with websockets.connect(url) as websocket:
            while True:
                print("hi")
                wss_res = await websocket.recv()
                await queue.put(json.loads(wss_res))

class Task: 

    def __init__(self, url : str, provider_name: str):
        
        self.name = provider_name
        self.query = url
        self.protocol = url.split(':')[0]

        self._task : Dict[Callable[..., Any], str] = {Wss.listen if self.protocol == 'wss' else Http.req : self.query}
        self.priority : int
    
    def new_push(self):
        func, query = self._task.items()
        return func(query)



class Array(ABC):
    
    def __init__(self) -> None:
        self.queue = Queue()

    def size(self):
        return self.queue.qsize()
    @abstractmethod
    def load():
        pass

class Buffer(Array):

    def __init__(self):
        super().__init__()

    async def load(self, task : Task):
        name_provider, protocol, action, data = task.push()
        task = asyncio.create_task(action(data), name= name_provider+'.'+protocol,)
        await self.queue.put(task)
    
    async def execute_task(self):
        while True:
            task: asyncio.Task = await self.queue.get()
            self.res = await task
            return self.res
