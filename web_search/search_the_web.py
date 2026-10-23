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
        self.wrapper = DuckDuckGoSearchAPIWrapper(
                    region="us-en",                     # exclude wt-wt"
                     backend="auto"
                )
    #search the web function
    def web_search_query(self,query:str,max_results:int)-> List[str]:
        try:
            #return links by iterating through the results
            return [r["link"] for r in self.wrapper.results(query, max_results)]

       
        except Exception as e:
            # catches DDGSException, rate limit, timeout
            raise RuntimeError(f"Search failed for '{query}': {e}") from e



