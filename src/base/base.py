from typing import Optional, List, Dict, Set, Union, Tuple, Any, Callable
from secret.secret_man.secret_man import SecretManager as sm
from abstract import  Task, Buffer
from abc import ABC, abstractmethod
import aiohttp
import asyncio
from asyncio.queues import Queue
import multiprocessing.queues
import json


# each provider needs a stack of tasks and all the provider togheter made up another stack

class Provider(ABC):

    def __init__(self, **args) -> None:

        if any(var is None for var in list(args.values())):
            raise ValueError('values must not be None')

        self.name : str = args.get('name', '')
        self.base_url  : Union[List[str], str] = args.get('base_url', '')
        self.auth : Dict[Any, Any] = args.get('auth', {})
        self.limit : Union[Tuple[Tuple[int, int]], Tuple[int, int]] = args.get('limit', ())


    @staticmethod
    @abstractmethod
    def config() -> Dict[str, str]:
        pass
    
    @abstractmethod
    def compose_task(): pass

    def create_task(self, param):
        return Task(
            url= self.compose_task(),
            provider_name= self.name)

    @staticmethod
    def taskarray_load(task : Task) -> None:
        TaskArray.add_task(**task)
    


class TaskArray(Buffer):
    """A stack that implements random access.
    Element are instruction to excecute, like 
    an http request or a wss connection
    """

    def __init__(self, task: Task) -> None:
        self.task = task
        self.add_producer(task=task)


    def exec_task(self):
        while True:
            self.task.res = super().get_data(self.task)

    def order(self):
        pass

    @classmethod
    def execute(cls, task : Task):
        cls._Array._use(cls.req(**task)) # chage params to payload



    

    
    
