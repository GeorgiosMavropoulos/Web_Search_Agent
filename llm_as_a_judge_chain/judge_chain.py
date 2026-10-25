"""This class is the last  link of the chain. It contains a method which passes the JUDGE PROMPT to the llm with the translated text and the original summary"""
from llm.llm_instance import LLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from prompts.prompt_templates import Prompt_Temps
from translation_chain.translator_chain import TranslatorChain
prompt_template = Prompt_Temps()
translator= TranslatorChain()
llm_client = LLM()

class JudgeChain:
    def __init__(self):
        pass


    #function to judge the translated text
    
    def judge_text(self,user_question:str)->str:
        #call translation runnable to get the translation
        translation_runnable = translator.translator_runnable()
        ##add the trans runnable to the chain
        judge_chain = (
        RunnableParallel({
            #keep the initial question
            "summarized_content": RunnablePassthrough(), 
            "translated_texts": translation_runnable 
        })
        | prompt_template.JUDGE_TEMPLATE
        | llm_client.get_llm()
        | StrOutputParser()
    )

        #return the scores
        scores = judge_chain.invoke(user_question)
        return scores

judge_instance = JudgeChain() 
test = judge_instance.judge_text('Who is Jason Vorhees')
print(test)