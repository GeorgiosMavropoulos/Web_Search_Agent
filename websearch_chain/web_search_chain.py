"""This file contains a method with the webseach chain. This chain get's user's input, calls the web search methods to execute the requested queries
and returns the retrieved URLs
"""
#import the llm instance
from llm.llm_instance import LLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
import json
from prompts.prompt_templates import Prompt_Temps
from web_search.search_the_web import WebSearch
#initialize an llm object
llm_client = LLM()

prompt_template = Prompt_Temps()

search_the_web = WebSearch()
class WebSearchChain:

      @staticmethod
      def generate_search_queries(user_question: str):
        web_search_query_chain = ({
            "user_question": RunnablePassthrough(),
            "num_search_queries": RunnableLambda(lambda x: 5)
        }
                            |prompt_template.WEB_SEARCH_PROMPT_TEMPLATE|
                            llm_client.get_llm()
                            |StrOutputParser()| RunnableLambda(json.loads))

        #invoke the chain to call the llm and delegate the generated queries into a variable
        queries = web_search_query_chain.invoke(user_question)     
        
        return queries

    
      @staticmethod
      #the following functions searches the web with web search function. The generated queries are being passed as arguments on the websearch function
      def execute_web_search(queries: list[str]):
       
         urls = []
         for query in queries:
                try:
                    urls.extend(search_the_web.web_search_query(query, 5))
                except RuntimeError as e:
                    print(e)  # continue to next query
         return list(dict.fromkeys(urls))


      #method to call generate queries and search the web for relevant urls
      @staticmethod
      def search(user_question: str):
        queries = WebSearchChain.generate_search_queries(user_question)
        urls = WebSearchChain.execute_web_search(queries)
        return urls

      #pass this method to runnable lambda in order to add it into scrapper chain
      search_runnable = RunnableLambda(search)






           
                       

      
  
    
                    
                   

