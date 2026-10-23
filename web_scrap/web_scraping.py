"""This module contains the function which receives a url as input and cleans 
all the gibberish with beautifull soup, in order to handle only plain text to the agent"""
import requests
from bs4 import BeautifulSoup
class WebScrap:
    def __init__(self):
        pass


    #function to scrap the webpage
    def web_scraper(self,url:str)->str:
        try:
            #create the headers to camouflage the agent so websites won't block it
            headers = {
                            "User-Agent": (
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/124.0.0.0 Safari/537.36"
                            ),
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                            "Accept-Language": "en-US,en;q=0.5",
                            "Upgrade-Insecure-Requests": "1",
                            "Cache-Control": "max-age=0"
                        }
            response = requests.get(url=url,headers=headers,timeout=15)

            #validate whether response is 200 ok! or not
            if response.status_code == 200:
                #parse the html elements
                soup = BeautifulSoup(response.text,'html.parser')
                page_text = soup.get_text(' ',strip=True)

                #return an error message if page does not contain text
                if not page_text.strip():
                    raise ValueError('This webpage does not contain readable text') 
                
                return page_text

            #return an error message if response is not ok!
            else:
                raise RuntimeError(f'Scraping failed due to error: {response.status_code}')

        #return exceptions
        except AttributeError as e:
            raise RuntimeError(f'Error while editing content') from e
        except RuntimeError as e:
            raise RuntimeError(f'Invalid url') from e
        except Exception as e:
            raise RuntimeError(f'Error, cannot fetch the text, please try again later.') from e
