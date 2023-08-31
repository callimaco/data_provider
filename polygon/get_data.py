"""this module takes data from various end points"""

from typing import Optional
from secret.secret_man.secret_man import SecretManager as sm
import requests

class Base:
    name = 'polygon'
    base_url = 'https://api.polygon.io'
    auth = {
           'Authorization': f'Bearer {sm.getkey(name)}'
        }
    request_limit_per_minute = 5
    time_in_seconds = 60
    waiting_time = time_in_seconds / request_limit_per_minute

class Ticker(Base):

    end_point = '/v3/reference/tickers'
    min_results_per_page = 100
    max_results_per_page = 1000
    
    def __init__(self,
                 ticker: Optional[str] = None,
                 limit: Optional[int] = max_results_per_page) -> None:
        self.next_url = None
        self._tiker_code = ticker
        if not (
            (limit >= Ticker.min_results_per_page) 
            and 
            (limit <= Ticker.max_results_per_page)
            ):
            raise ValueError("Limit must belong to [100:1000] interval")
        self.results_per_page = limit


    def data_getter(self) -> None:
        """:param payload: parameters of the query to issue trought requests"""
        self.flag = True

        if self.next_url == None: 
            query = Base.base_url + Ticker.end_point
            self.payload = {'tiker' : self._tiker_code, 'limit' : self.results_per_page}
        else: 
            query = self.next_url
            self.payload = {'limit' : self.results_per_page}
            
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

