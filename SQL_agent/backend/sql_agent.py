'''
Script that creates a retail SQL agent to form a Q&A tool where questions relate to information stored in a retail database related to t-shirts.
The SQL agent created connects to the requisite database and pulls data from the necessary columns using necessary SQL queries.
'''
# import necessary libraries/frameworks/modules
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ProviderStrategy
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from pathlib import Path
from functools import lru_cache

#.env path
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# fetch API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# fetch necessary DB credentials
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
localhost = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

# choose database
db_name = 'atliq_tshirts'

# create DB URI with above credentials
db_uri = f'mysql+mysqlconnector://{user}:{password}@{localhost}:{port}/{db_name}'

# setup connection to MYSQL database Atliq_tshirt using above URI
db = SQLDatabase.from_uri(db_uri)

# setup OPENAI model
model = ChatOpenAI(
    model='gpt-5.2',
    api_key=openai_api_key,
    temperature=0.3, # higher number indicates more randomness in the model's output
    max_tokens=500, #defines the no of words in the model's response
    timeout=30 # max time in sec to wait for model's response
)

# setup toolkit for db interaction
mysql_toolkit = SQLDatabaseToolkit(db=db,llm=model)

# Get the different tools for the model to interact and fetch results from the database such as sql_db_query, sql_db_query_checker, sql_db_list_tables & sql_db_schema.
tools = mysql_toolkit.get_tools()

# setup a detailed system prompt to customise agent behaviour.
system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. DO NOT skip this step.

NEVER expose internal identifiers such as IDs, primary keys, or surrogate keys. ALWAYS return human-readable attributes instead.

NEVER show texts wrapped with ** around. ALWAYS display clean texts in response.

NOTE that the price column in t_shirts table has the unit of Rs.

Then you should query the schema of the most relevant tables.

Few-Shot Examples:

User: What is the total revenue for Levi brand? 
SQL:
SELECT
  SUM(ts.stock_quantity * ts.price * (1 - COALESCE(d.pct_discount, 0)/100)) AS revenue
FROM t_shirts ts
LEFT JOIN discounts d ON d.t_shirt_id = ts.t_shirt_id
WHERE ts.brand = 'Levi';

User: Which T-shirt has the lowest discount? 
SQL:
SELECT
  ts.brand,
  ts.color,
  ts.size,
  d.pct_discount
FROM t_shirts ts
JOIN discounts d ON d.t_shirt_id = ts.t_shirt_id
ORDER BY d.pct_discount ASC
LIMIT 1;
""".format(
    dialect=db.dialect,
    top_k=5,
)

# setup & run the agent with structured output
class Output(BaseModel):
    answer : str = Field(description='Final answer to user query')

# setup agent
sql_agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)
@lru_cache
def fetch_response(query : str):
    '''
    Function that runs the SQL agent given a user query and returns the answer.
    :return:
    '''
    result = ""
    for token,metadata in sql_agent.stream({"messages":[{"role":"user","content":query}]},stream_mode="messages"):
        node = metadata['langgraph_node']
        content = token.content_blocks

        if node == 'model' and content and content[0].get('text',''):
            result += content[0]['text']
            yield result


# if __name__ == '__main__':
#     query = "Suppose we sell all the t-shirts today in our inventory with their respective discounts applied. Display all the revenues that would be generated across brands?"
#     print(f'{query}')
#     fetch_response(query)
