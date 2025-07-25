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
    user_msgs = sum(1 for m in st.session_state.get("messages", []) if m["role"] == "user")
    ai_msgs = sum(1 for m in st.session_state.get("messages", []) if m["role"] == "ai")
    st.markdown(f"**💬 Messages:** {user_msgs + ai_msgs}")
    st.markdown(f"- You: {user_msgs}")
    st.markdown(f"- AI: {ai_msgs}")
    
    # Reset chat
    if st.button("🔁 Reset Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.markdown("### 💬 Chat with the AI Therapist")
for msg in st.session_state.messages:
    role = "🧑 You" if msg["role"] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {msg['content']}")

# Chat input
user_input = st.text_input("Type your message:", key="user_input", placeholder="What's on your mind?")

# Send button
if st.button("Send", use_container_width=True):
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("AI is thinking..."):
            ai_response = run_chat(user_input)
        st.session_state.messages.append({"role": "ai", "content": ai_response})
        st.experimental_rerun()
