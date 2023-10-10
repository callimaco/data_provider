from ...core.base import Provider, TaskArray, Task
from ...core.constants import *
from secret.secret_man.secret_man import SecretManager as sm
from typing import Optional, Dict
from abc import ABC, abstractclassmethod
import urllib3

from ...tool.util import concat



class Polygon(Provider):

    """polygon"""

    @staticmethod
    def config():
        return{
              name : 'polygon',
              base_url : r"https://api.polygon.io",
              auth : {"Authorization": f"Bearer {sm.getkey(name= 'polygon')}"},
              request_limit_per_minute : 5 
            }

    def __init__(self,**config) -> None:
        super().__init__(**config)


class Hybrid(Polygon, TaskArray):
    """yeah"""


class Tickers(Hybrid):
    _min_results_per_page = 100
    _max_results_per_page = 1000

    end_point = '/v3/reference/tickers'
    
    def __init__(self,
                 ticker: Optional[str] = None,
                 limit: Optional[int] = _max_results_per_page) -> None:
        super().__init__()
        TaskArray.__init__(self.create_task(param='endpoint' + 'ticker'))

        self.next_url = None
        self._tiker_code = ticker
        self.results_per_page = limit
        

    def compose_task(self, param) -> None:
        """:param payload: parameters of the query to issue trought requests"""
        self.flag : bool = True
        if self.next_url is None: 
            self.query : str = self.base_url + self.end_point
            self.payload : Dict = {'tiker' : self._tiker_code, 'limit' : self.results_per_page}
        else: 
            self.query = self.next_url
            self.payload = {'limit' : self.results_per_page}
        
        self.query = {self.query: self.payload}
        return 'a'

##### I can split here, above the logit to implement for each provider
##### Below the one to implement in Internet
        res = requests.get(
                    query,
                    params= self.payload,
                    headers= self.auth)
        
        self.status = res.status_code
        
        try:
            self.next_url = res.json()['next_url']
        except KeyError:           
            self.flag = False
        finally:
            self.results = res.json()['results']
