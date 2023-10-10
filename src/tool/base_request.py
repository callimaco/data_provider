"""this module takes data from various end points"""

from typing import Optional, List, Dict
from secret.secret_man.secret_man import SecretManager as sm
import requests

class Base:


    _name: str
    _base_url : str
    _auth : Dict[str, str]
    _instances : List[object]
    request_limit_per_minute : int
    minute : int #in seconds
    waiting_time =int
    
    @property
    def number_of_instances(self) :
        return len(self._instances) 
    @property
    def _scheduler(self):

        return 

class Ticker(Base):
    
    _min_results_per_page = 100
    _max_results_per_page = 1000

    end_point = '/v3/reference/tickers'
    
    def __init__(self,
                 ticker: Optional[str] = None,
                 limit: Optional[int] = _max_results_per_page) -> None:
        
        self._instances += 1

        self.next_url = None
        self._tiker_code = ticker
        if not (
            (limit >= Ticker._min_results_per_page) 
            and 
            (limit <= Ticker._max_results_per_page)
            ):
            raise ValueError("Limit must belong to [100:1000] interval")
        self.results_per_page = limit


    def data_getter(self) -> None:
        """:param payload: parameters of the query to issue trought requests"""
        self.flag = True

        if self.next_url is None: 
            query = Base.base_url + Ticker.end_point
            self.payload = {'tiker' : self._tiker_code, 'limit' : self.results_per_page}
        else: 
            query = self.next_url
            self.payload = {'limit' : self.results_per_page}


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

