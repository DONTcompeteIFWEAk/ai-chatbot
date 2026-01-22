import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="My AI Chatbot", layout="centered")

st.title("My AI Chatbot")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")

# Input box
user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send to backend
    response = requests.post(API_URL, json={"message": user_input})
    ai_reply = response.json()["reply"]

    # Add AI message
    st.session_state.messages.append({"role": "ai", "content": ai_reply})

    st.experimental_rerun()
