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

    #function to translate the text
    def translate(self, user_question: str):

        summary_runnable = SummaryChain.summary_runnable()

        translate_chain = (
            RunnableLambda(
                lambda question: {
                    "summarized_content": summary_runnable.invoke(question) #pass the generated summary to the chain
                }
            )
            | RunnableParallel({
                "summarized_content": RunnableLambda(
                    lambda x: x["summarized_content"]
                ),
                "translated_texts": (
                    prompt_template.TEXT_TRANSLATE_TEMPLATE
                    | llm_client.get_llm()
                    | StrOutputParser()
                )
            })
        )

        translation = translate_chain.invoke(user_question)

        print("Translation:\n", translation)

        return translation


    #translator runnable
    @staticmethod
    def translator_runnable() -> RunnableLambda:
            """Runnable: user_question (str) -> summary from summary runnable (str), translation (str)."""
            return RunnableLambda(lambda q: TranslatorChain().translate(q))
