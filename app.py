import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from src.workflows.db_query.workflow import run_query

st.set_page_config(page_title="DB Query Chat", layout="wide")
st.title("Database Query Chat Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the database..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response = run_query(
                user_query=prompt,
                conversation_history=st.session_state.messages[:-1]
            )
            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
    
    st.rerun()

if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()
