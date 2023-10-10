from ...core.base import Provider, TaskArray, Task
from ...core.constants import *
from secret.secret_man.secret_man import SecretManager as sm
from typing import Optional
import urllib3
from ...tool.util import concat



class Nasdaq(Provider):

    """nasdaq"""

    @staticmethod
    def config():
        return{
              'name' : 'nasdaq',
              'base_url' : rf"https://data.nasdaq.com/data",
              # https://data.nasdaq.com/api/v3/datasets/FRED/GDP.csv?collapse=annual&rows=6&order=asc&column_index=1&api_key=YOURAPIKEY
              'auth' : {"Authorization": f"api_key={sm.getkey(name= 'nasdaq')}"},
              'request_limit_per_minute' : 5 
            }

    def __init__(self,**config) -> None:
        super().__init__(**config)
        
        self.protocols = self.base_url.split(sep=':')[0]