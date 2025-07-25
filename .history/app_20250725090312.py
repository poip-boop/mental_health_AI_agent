import streamlit as st
from therapist_ai import run_chat
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Mental Health AI Therapist", layout="centered")

st.title("🧠 Mental Health AI Therapist")
st.caption("Your private and compassionate space to talk.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("How are you feeling today?")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    response = run_chat(user_input)
    st.session_state.chat_history.append(("therapist", response))

for role, msg in st.session_state.chat_history:
    with st.chat_message(name=role):
        st.markdown(msg)
