"""This file contains a class with prompt templates"""
from langchain_core.prompts import PromptTemplate

class Prompt_Temps:
    def __init__(self):
        pass


    #web-search assistant's template
    WEB_SEARCH_INSTRUCTIONS = """
                  You are a web research assistant.

Given the user's question, generate {num_search_queries}
distinct web search queries that will help find reliable,
relevant information.

User question:
{user_question}

Requirements:
- Each query should explore a useful aspect of the question.
- Avoid duplicate or nearly identical queries.
- Use specific keywords that are likely to return relevant sources.

Return only a valid JSON array of strings.

Example:
[
    "history and main attractions of Astorga Spain",
    "best things to do in Astorga Spain",
    "Astorga Spain local culture and tourism"
]
                  
                    """
    WEB_SEARCH_PROMPT_TEMPLATE = PromptTemplate.from_template(template=WEB_SEARCH_INSTRUCTIONS)




    #Web scrapper assistant template
    WEB_SUMMARIZER_INSTRUCTIONS = """
                                 You are a research assistant.

                            Summarize the following web page content in a clear,
                            accurate, and concise way.

                            User question:
                            {user_question}

                            Web page content:
                            {search_result_text}

                            Requirements:
                            - Focus on information relevant to the user's question.
                            - Preserve important facts, names, dates, and statistics.
                            - Do not invent information that is not present in the source.
                            - Avoid unnecessary repetition.
                            - If the content does not contain relevant information,
                            clearly state that.

                            Return only the summary.
                             
                                    """
    TEXT_SUMMARY_TEMPLATE = PromptTemplate.from_template(template=WEB_SUMMARIZER_INSTRUCTIONS)


    TEXT_TRANSLATOR_INSTRUCTIONS = """
                                   You are a professional translator.

                                    Translate the following research summary into Greek,
                                    Italian, and French.

                                    Summary:
                                    {summarized_content}

                                    Requirements:
                                    - Keep the original meaning.
                                    - Preserve names, dates, numbers, and factual details.
                                    - Use natural, grammatically correct language.
                                    - Do not add new information.

                                    Organize the output under these headings:
                                    Greek:
                                    Italian:
                                    French:
                                   """

    TEXT_TRANSLATE_TEMPLATE = PromptTemplate.from_template(template=TEXT_TRANSLATOR_INSTRUCTIONS)




    JUDGE_INSTRUCTION = """
                        You are a translation evaluator.

                        Evaluate the translations by comparing them with the original text.

                        Original text:
                        {summarized_content}

                        Translations:
                        {translated_texts}

                        For each language:
                        - Give an overall score from 0 to 100.
                        - Evaluate meaning preservation, fluency, completeness,
                        and factual accuracy.
                        - Explain the main reasons for the score.
                        - Identify any mistranslations or missing information.

                        Return the results in clearly labeled sections.
                        """