'''
Script that creates an UI that answers questions basis news articles with the help of a tool based RAG agent.
'''

import streamlit as st
from NewsResearchTool.backend.tool_based_RAG import call_rag_agent, index_documents_to_vector_db
from NewsResearchTool.backend.speech_to_text import transcribe_audio
from NewsResearchTool.backend.text_to_speech import text_to_speech
import asyncio

st.markdown("""
<style>
/* Force audio input to match text_input height */
div[data-testid="stAudioInput"] {
    height: 42px;
    display: flex;
    align-items: center;
    margin-top: 30px;
}

/* Inner wrapper */
div[data-testid="stAudioInput"] > div {
    height: 100%;
    padding: 0 8px !important;    /* reduce vertical padding */
    display: flex;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

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

with st.container(border=True):
    col1, col2 = st.columns([5,2])

    # initialise state
    if 'text_question' not in st.session_state:
        st.session_state.text_question = ''

    # setup audio I/P
    with col2:
        audio = st.audio_input(label='Audio:',label_visibility='collapsed')
        # in case audio exists transcribe it to text and place it in question tab.
        if audio:
            with st.spinner('Processing Audio...'):
                st.session_state.text_question = transcribe_audio(audio)

    # setup question input
    with col1:
        question = st.text_input(label='Question:',value="",placeholder='Enter a question to get answer for',key='text_question')

    submitted = st.button(label="Get answer",help="Process Question",type="primary")

    # check if both question and urls are present in which case fetch LLM response
    if st.session_state.text_question and urls and submitted:
        # set empty container to write answer to.
        placeholder = st.empty()
        full_response = ""
        for response in call_rag_agent(question,tuple(urls)):
            placeholder.write(response)
            full_response = response

        # convert response to audio
        asyncio.run(text_to_speech(full_response))

    elif st.session_state.text_question and not urls:
        st.write('No valid url provided.Please provide url and try again')
    elif not st.session_state.text_question and urls:
        index_documents_to_vector_db(tuple(urls))








