"""This file contains a class with the summary method. The summary method calls the Lambda runnable from the scrap chain function to provide a question.
this functions uses the lambda runnable from the websearch. The last runnable generated 5 queries and find 5 relevant URLS. Then the scrap runnable
scraps the webpages to generate a coherent text.
"""
from llm.llm_instance import LLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
import json
from prompts.prompt_templates import Prompt_Temps
from scrapper_chain.scrap_chain import WebScrapChain
#initialize an llm object
llm_client = LLM()

scrap_obj = WebScrapChain()
prompt_template = Prompt_Temps()

class SummaryChain:
    def __init__(self):
     pass

    #function to create the summary chain
    def generate_summary(user_question:str)-> str:
 
       #create the summary chain and add summary's prompt template
       summary_chain = (prompt_template.TEXT_SUMMARY_TEMPLATE|llm_client.get_llm()|StrOutputParser())

       #create the research_chain
       research_chain = (
            RunnableLambda(WebScrapChain.scrap_texts) #call runnable lambda from scrap texts 
            | RunnableLambda(
                lambda search_result_text: {
                    "text": "\n\n".join(search_result_text)
                }
            )
            | summary_chain
        )

       summary = research_chain.invoke(user_question)
       return summary

summary = SummaryChain.generate_summary('Who is Michael Jordan?')
                                   
                                   