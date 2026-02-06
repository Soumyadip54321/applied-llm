'''
Script that demonstrates usage of tool-based RAG agent to fetch answers to user queries pertaining to news articles from some
popular websites.
'''
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_classic.embeddings import CacheBackedEmbeddings
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.tools import tool
import os
from langchain_classic.storage import LocalFileStore
from functools import lru_cache

#.env path
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# fetch API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# create a cache in disk to store embeddings of text once generated
store = LocalFileStore("./cache/")

# create model
model = ChatOpenAI(
    model='gpt-5.2',
    api_key=openai_api_key,
    temperature=0.3, # higher number indicates more randomness in the model's output
    max_tokens=500, #defines the no of words in the model's response
    timeout=30 # max time in sec to wait for model's response
)

@lru_cache
def index_documents_to_vector_db(urls : tuple):
    '''
    Function that fetches articles using urls, converts them to fixed-size vectors and store them in vector database
    for fast retrieval using similarity search.
    parameters: urls (tuples of strings)
    :return: vector database
    '''

    # initialize url loader with the URLs of all the news articles & create langchain documents. Each document has attributes such as page_content & metadata.
    url_loader = UnstructuredURLLoader(list(urls))
    news_docs = url_loader.load()

    # use text-splitter to create chunks/document-splits for easy indexing later on from vector database
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,length_function=len,add_start_index=True)
    chunks = text_splitter.split_documents(news_docs)

    # setup embedding model to convert chunks/document-splits to numerical fixed-sized vectors
    embedding = OpenAIEmbeddings(api_key=openai_api_key)

    # wrap embedding with cache so that for repeated docs embeddings are fetched from cache rather than re-generated.
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(underlying_embeddings=embedding,document_embedding_cache=store,namespace=embedding.model)

    # setup lightweight vector database with embeddings & add documents to the database such that they get automatically converted to vectors
    vector_store = InMemoryVectorStore(embedding=cached_embedder)
    ids = vector_store.add_documents(chunks)

    return vector_store

def create_retrieve_tool(vector_store):

    @tool
    def retrieve_context_with_tool_based_rag(query : str):
        '''
        Function that fetches relevant documents from vector database basis user query.
        :param query:
        :return: relevant documents from vector database
        '''

        # fetch the most relevant document form database basis query
        retrieved_docs = vector_store.similarity_search(query,k=2)

        # create output from each relevant documents as Source: Document link; Content: Document content.
        serialized = "\n\n".join(f"Source: {doc.metadata}\n Content: {doc.page_content}" for doc in retrieved_docs)

        return serialized

    return retrieve_context_with_tool_based_rag

def call_rag_agent(query : str, urls):
    '''
    Function that creates RAG agent for user query.
    :param query: user query
    :param urls: url of news articles to fetch data from
    :return: LLM RAG agent output just like chat bot does with text appearing progressively.
    '''

    # build vector store ONCE
    vector_store = index_documents_to_vector_db(urls)

    # create retrieval tool that captures vector_store
    retrieve_tool = create_retrieve_tool(vector_store)

    output = ""

    # setup RAG agent
    agent = create_agent(
        model=model,
        tools=[retrieve_tool])

    for token,metadata in agent.stream({"messages":[{"role":"user","content":query}]}, stream_mode="messages"):
        node = metadata['langgraph_node']
        content = token.content_blocks

        if node == 'model' and content and content[0].get('text', ''):
            # capture progressively increasing response
            output += content[0]['text']
            yield output


# if __name__ == '__main__':
#     url_tuples = tuple('https://www.moneycontrol.com/news/business/tata-motors-mahindra-gain-certificates-for-production-linked-payouts-11281691.html')
#     Query = 'What is production linked payouts?'
#     print(call_rag_agent(Query, url_tuples))