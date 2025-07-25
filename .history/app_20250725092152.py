import streamlit ppias st
from therapist_ai import run_chat
from crisis import SAFETY_MESSAGE

st.set_page_config(page_title="Mental Health AI Agent", page_icon="🧠", layout="centered")
st.title("🧠 Mental Health AI Agent")
st.markdown("A compassionate AI therapist to support your mental well-being. Ask anything.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("How are you feeling today?")
if user_input:
    response = run_chat(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Therapist", response))

for speaker, message in st.session_state.chat_history:
    with st.chat_message(name=speaker):
        st.markdown(message)
