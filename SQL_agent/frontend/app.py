'''
Script that displays Atliq T Shirts database Q&A UI on streamlit that displays response fetched from RAG SQL-Agent in the backend
given a user question.
'''

import streamlit as st
from SQL_agent.backend.sql_agent import fetch_response

import streamlit as st

st.title(":blue[AtliQ] :red[T-Shirt]: Database Q&A 👕")

with st.form(key='question_form', clear_on_submit=False,enter_to_submit=True):
    # fetch user question
    question = st.text_input("Ask any question:",value="",placeholder="Please enter a question",help="Enter a question below to get answer.")
    submitted = st.form_submit_button(label="Get answer",type="primary")

    # if there is a question fetch response by running the RAG SQL-Agent in the backend.
    if question and submitted:
        result = fetch_response(question)
        st.write('Answer:',result)

