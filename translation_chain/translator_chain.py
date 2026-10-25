"""This file contains the class for the translator. It receives the summarized text and translate it into 3 languages and adds the text into the chain"""
from llm.llm_instance import LLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda,RunnableParallel,RunnablePassthrough

from prompts.prompt_templates import Prompt_Temps
from summary_chain.summary_chain_implementation import SummaryChain
prompt_template = Prompt_Temps()
llm_client = LLM()
class TranslatorChain:
    def __init__(self):
        pass

    #function to translate
    def translate(self,user_question: str):
      #call summary runnable to run the summary
      summary_runnable = SummaryChain.summary_runnable()

      #pass summary runnable to the chain 
      translate_chain = RunnableParallel({
            # store summary to transfer it to the judge
            "summarized_content": RunnablePassthrough(),
            # produce the summary and store it to the template with the translated text
            "translated_texts": (
                RunnableLambda(lambda summary: {"summarized_content": summary})
                | prompt_template.TEXT_TRANSLATE_TEMPLATE
                | llm_client.get_llm()
                | StrOutputParser()
            )
        })
      translation = translate_chain.invoke(user_question)
      return translation


    #translator runnable
    @staticmethod
    def translator_runnable() -> RunnableLambda:
            """Runnable: user_question (str) -> summary from summary runnable (str), translation (str)."""
            return RunnableLambda(lambda q: TranslatorChain().translate(q))
