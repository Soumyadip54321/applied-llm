'''
Script that uses Perplexity model sonar to fetch fictitious restaurant and menu list basis user prompts on UI.
'''

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
from dotenv import load_dotenv
import os

#.env path
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# fetch API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# create agent using Sonar-pro model and configure other model related params
model = ChatOpenAI(
    model='gpt-5.2',
    api_key=openai_api_key,
    temperature=0.3, # higher number indicates more randomness in the model's output
    max_tokens=500, #defines the no of words in the model's response
    timeout=30 # max time in sec to wait for model's response
)

def generate_restaurant_and_menu(cuisine):
    '''
    Function that generates restaurant and menu list given the country the restaurant belongs to.
    parameters: restaurant_name
    :return:
    '''

    # setup a message template
    prompt = ChatPromptTemplate.from_template('''
    I want to open a restaurant for {cuisine} food. Suggest a fancy name for it? 
    
    Only one name please.
    Do not add '**' at the start and end of the restaurant name.
    Do not add any description following the name like "The Grand Hotel. It's a classic place..." just "The Grand Hotel"
    Do not add citations at all like [1][2].. following the restaurant name.
    ''')

    # display response from the model using runnable sequence
    name_chain = prompt | model | StrOutputParser()

    # generate menu items based on restaurant name using runnable sequence
    menu_prompt = ChatPromptTemplate.from_template('''
    Suggest some menu items for {restaurant_name}. 
    
    Do not add citations like [1][2][3]...
    Do not add explanations at all.
    Do not add any description after the food names.
    
    Return it as a comma separated strings like 'fooditem1,fooditem2,fooditem3,...'
    ''')
    menu_chain= menu_prompt | model | StrOutputParser()

    # sequential chain
    full_chain = (
        {'restaurant_name':name_chain} | RunnablePassthrough.assign(menu=menu_chain)
    )

    result = full_chain.invoke({'cuisine':cuisine})
    return result

if __name__ == '__main__':
    print(generate_restaurant_and_menu('Mongolian'))