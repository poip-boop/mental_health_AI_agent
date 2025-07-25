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
    st.markdown("**⚠️ This is not a substitute for professional help.**")

# Session storage for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat display
st.markdown("### 💬 Chat with the AI Therapist")
for msg in st.session_state.messages:
    role = "🧑 You" if msg["role"] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {msg['content']}")

# Input area
user_input = st.text_input("Type your message:", key="user_input")

if st.button("Send", use_container_width=True):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("AI is thinking..."):
            ai_response = run_chat(user_input)
        st.session_state.messages.append({"role": "ai", "content": ai_response})
        st.experimental_rerun()
