"""This file contains the chain which receives the retrieved urls and scraps the content to get valid text"""

from langchain_core.runnables import RunnableLambda
from typing import List
from websearch_chain.web_search_chain import WebSearchChain
from web_scrap.web_scraping import WebScrap

web_scraper = WebScrap()
search_web_chain = WebSearchChain()
class WebScrapChain:
    def __init__(self):
        pass

    #method to scrap the urls
    def scrape_urls(urls: list[str]) -> list[str]:
        texts = []

        for url in urls:
            try:
                text = web_scraper.web_scraper(url)

                if text and text.strip():
                    texts.append(text)

                else:
                    print(
                        f"Skipping URL with empty text: {url}"
                    )

            except Exception as e:
                print(
                    f"Skipping URL '{url}': {e}"
                )
                continue

        if not texts:
            raise RuntimeError(
                "No text could be retrieved from the search results."
            )

        return texts

    #function to get the retrieved URLs and scrap the web
    @staticmethod
    def scrap_texts(user_question: str) -> list[str]:

            #this lambda runnable with search method generates the queries and queries the web to find relevant URLs
            search_runnable = RunnableLambda(search_web_chain.search)

            
            #create a scrap runnable
            scrap_runnable = RunnableLambda(WebScrapChain.scrape_urls)

            #create the chain
            scrap_chain = (search_runnable| scrap_runnable )
            
            return scrap_chain.invoke(user_question)


text = WebScrapChain.scrap_texts("Who is Michael Jordan?")
print("Final result:", text)


text = WebScrapChain.scrap_texts('Who is Michale Jordan?')
print(text)


