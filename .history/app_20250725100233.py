import streamlit as st
from therapist_ai import run_chat
from crisis import SAFETY_MESSAGE

# Page settings
st.set_page_config(
    page_title="Mental Health AI Agent 🧠",
    page_icon="🧠",
    layout="wide",
)

# Header
st.markdown(
    """
    <h1 style='text-align: center; color: #4B8BBE;'>🧠 Mental Health AI Agent</h1>
    <p style='text-align: center;'>A supportive and safe space powered by AI — built with ❤️ for wellness.</p>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.title("ℹ️ About")
    st.markdown("This AI agent uses advanced language models to offer mental health support, conversation, and guidance.")
    st.markdown(SAFETY_MESSAGE)
    
    # Chat tracker
    user_msgs = sum(1 for m in st.session_state.get("messa
