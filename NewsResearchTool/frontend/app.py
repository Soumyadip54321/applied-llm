'''
Script that creates an UI that answers questions basis news articles with the help of a tool based RAG agent.
'''

import streamlit as st
from NewsResearchTool.backend.tool_based_RAG import call_rag_agent, index_documents_to_vector_db

# set page title
st.title('News :red[_Research_] Tool')

urls = []

# set sidebar
with st.sidebar:
    with st.form(key='url_form',enter_to_submit=True,clear_on_submit=False):
        st.subheader('News Article URLs')
        url1 = st.text_input(label='URL1', value="",placeholder='Enter a URL to get news articles from')
        url2 = st.text_input(label='URL2', value="", placeholder='Enter a URL to get news articles from')
        url3 = st.text_input(label='URL3', value="", placeholder='Enter a URL to get news articles from')

        # create process URLs button
        submitted = st.form_submit_button(label="Process URLs",help="Fetch articles and store in database",type="primary")

        # fetch urls if typed in
        if url1:
            urls.append(url1)
        if url2:
            urls.append(url2)
        if url3:
            urls.append(url3)

        # fetch articles from urls and store them in vector database upon having pressed the submit button and presence of at least one url.
        if submitted and urls:
            index_documents_to_vector_db(tuple(urls))

with st.form(key='question_form',enter_to_submit=False,clear_on_submit=False):
    question = st.text_input(label='Question:',value="",placeholder='Enter a question to fetch answer.')

    submitted = st.form_submit_button(label="Get answer",help="Process Question",type="primary")

    # check if both question and urls are present in which case fetch LLM response
    if question and urls and submitted:
        # set empty container to write answer to.
        placeholder = st.empty()
        for response in call_rag_agent(question,tuple(urls)):
            placeholder.write(response)
    elif question and not urls:
        st.write('No valid url provided.Please provide url and try again')
    elif not question and urls:
        index_documents_to_vector_db(tuple(urls))








