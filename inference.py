"""
Main Entry Point of the Application.

This module defines the Inference class, which serves as the main entry
point for the LLM-based web research and content validation application.

The application executes the following workflow:
1. Requests a query from the user.
2. Generates five search queries to retrieve relevant web information.
3. Finds relevant URLs and extracts the plain text from web pages.
4. Summarizes the extracted content.
5. Translates the summarized content into Greek, Italian, and French.
6. Passes the translated content to the judge chain for validation.
7. Displays the final result to the user.

The user can terminate the application by entering "bye".

Exceptions:
ValueError: Raised when the LLM processing encounters an invalid
value or an empty result, depending on the underlying chain.
Exception: Raised when a ValueError occurs during processing,
indicating that the LLM service is unavailable.
"""

from llm_as_a_judge_chain.judge_chain import JudgeChain

llm = JudgeChain()

class Inference:
    def __init__(self):
        pass


    
    def main():
     """Main method to call the judge and start this agent's lifecycle"""
     while True:
        try:
            #print a prompt so user can make a request to the LLM
            print('Press bye if you want to exit')
            user_question= str(input('Insert your query please: ')).upper() 

            if user_question == 'BYE'.strip():
               print('Goodbye to you too!')
               break

            #return an error message if user_quesiton is empty
            if not user_question.strip():
                print('Please, insert your request')
                continue

            #call the llm and pass the question
            result = llm.judge_text(user_question)

            #print result
            print(result)
            break
        #return an error message if result is empty
        except ValueError as e:
           raise Exception('LLM is unavailable right now')  from e

#call the main method
    if __name__== '__main__':

      main()
        
