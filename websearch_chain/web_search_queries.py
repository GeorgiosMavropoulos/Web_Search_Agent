"""This file contains a method with the webseach chain. This chain get's user's input, calls the web search methods to execute the requested queries
and returns the retrieved URLs
"""
#import the llm instance
from llm.llm_instance import LLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
import json
from prompts.prompt_templates import Prompt_Temps

#initialize an llm object
llm_client = LLM()
prompt_template = Prompt_Temps()
class WebSearchChain:
  
        web_search_query_chain = ({
            "user_question": RunnablePassthrough(),
            "num_search_queries": RunnableLambda(lambda x: 5)
        }
                            |prompt_template.WEB_SEARCH_PROMPT_TEMPLATE|
                            llm_client.get_llm()
                            |StrOutputParser()| RunnableLambda(json.loads))

        question = 'What can I see and do in the Spanish town of Astorga?'
        web_results = web_search_query_chain.invoke(question)
        print(web_results)
  
    
                    
                   

