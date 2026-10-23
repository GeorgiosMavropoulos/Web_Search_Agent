"""This file contains a class with a method which initialized the llm client using gemini"""
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class LLM:
    def __init__(self):
             
        self.GEMINI_MODEL = os.getenv('GEMINI_MODEL')
        self.GEMINI_API_URL = os.getenv('GEMINI_API_URL')
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

        required_vars = {
        "GEMINI_MODEL": self.GEMINI_MODEL,
        "GEMINI_API_URL": self.GEMINI_API_URL,
        "GEMINI_API_KEY": self.GEMINI_API_KEY,
    }

        missing_vars = [
        name for name, value in required_vars.items()
        if not value
    ]

        if missing_vars:
            raise ValueError(
            f"Missing environment variables: {', '.join(missing_vars)}"
        )
            
        try:
            #initialize the model
                self.llm = ChatOpenAI(
                model=self.GEMINI_MODEL,
                base_url=self.GEMINI_API_URL,  
                api_key=self.GEMINI_API_KEY,      
                temperature=0.6,
            )
        except Exception as e: #return an error message if cannot initialize the lang model
              raise RuntimeError(
                    "Failed to initialize the language model."
                ) from e
         
    #call the model
    def get_llm(self):
        if self.llm is not None:
            return self.llm
        else:
             raise RuntimeError('Cannot call the model')
