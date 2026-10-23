"""This file contains the function which receive's user's query and performs a websearch"""
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from duckduckgo_search.exceptions import (
   
    DuckDuckGoSearchException,
    RatelimitException,
    TimeoutException,
)
from typing import List

class WebSearch:
    def __init__(self):
        pass


    #search the web function
    def web_search_query(self,query:str,max_results:int)-> List[str]:
        try:
            #return links
            return [r["link"] for r in DuckDuckGoSearchAPIWrapper().results(query,max_results)]
                            #iterate through the results
                       
        
        #return a special exception if search fails
        except (DuckDuckGoSearchException) as e:
            raise Exception(f'Search error, please try again later:{e}')

        #exception if search hits rate limit
        except (RatelimitException) as e:
             raise Exception(f'Error, RateLimit hit the limits:{e}')

        #timeout exception
        except(TimeoutError) as e:
            raise Exception(f'Timeout error, please try again later:{e}')

        #General catch-all goes at the absolute bottom
        except Exception as e:
          raise Exception(f'An unexpected error occurred: {e}')


