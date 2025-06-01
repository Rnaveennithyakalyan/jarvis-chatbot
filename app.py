import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.set_page_config(page_title="J.A.R.V.I.S. Chatbot", layout="wide")

st.markdown("""
<style>
    body {
        background-color: #0d0d0d;
        color: #00ffea;
    }
    h1 {
        color: #00ffea;
        text-shadow: 0px 0px 10px #00ffea;
        text-align: center;
        font-size: 30px;
    }
    .chat-bubble {
        padding: 12px;
        border-radius: 8px;
        background-color: rgba(0, 255, 234, 0.1);
        color: #00ffea;
        border: 1px solid #00ffea;
        margin-bottom: 5px;
    }
    .stButton > button {
        background-color: #222222;
        color: #00ffea;
        border-radius: 10px;
        box-shadow: 0px 0px 10px #00ffea;
    }
    input::placeholder {
        color: transparent; /* Hide placeholder when inactive */
    }
    input:focus::placeholder {
        color: #888888; /* Show placeholder only when active */
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 J.A.R.V.I.S. AI Chatbot</h1>", unsafe_allow_html=True)

for message in st.session_state["messages"]:
    if message["role"] == "User":
        st.markdown(f"🧑 **User:** {message['content']}", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble'>🤖 **J.A.R.V.I.S.:** {message['content']}</div>", unsafe_allow_html=True)

user_input = st.text_input("Type your message...", key="user_input")

def call_gemini_api(user_query):
    response = model.generate_content(user_query)
    return response.text

if st.button("Send"):
    if user_input:
        reply = call_gemini_api(user_input)

        # Store chat history
        st.session_state["messages"].append({"role": "User", "content": user_input})
        st.session_state["messages"].append({"role": "J.A.R.V.I.S.", "content": reply})

        # Refresh UI after each message
        st.rerun()
    else:
        st.write(" Please enter a query before clicking Send!")