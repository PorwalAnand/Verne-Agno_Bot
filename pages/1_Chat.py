import streamlit as st
import datetime
from chatbot import get_response, get_knowledgebase_response
from agno_vernebot import create_verne_agno_agent

# --- Streamlit Page Config and Styling ---
st.set_page_config(page_title="Chat with VerneBot", layout="wide")

st.markdown("""
    <style>
    body, .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .stChatMessage, .markdown-text-container, .stMarkdown, p {
        color: #ffffff !important;
        font-size: 1.05rem;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stTextInput input {
        color: #ffffff !important;
        background-color: #2b2b2b !important;
    }
    .stTextInput > div > div > input {
        border: 1px solid #6a4caf;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: transparent !important;
        color: #cccccc !important;
        font-size: 0.85rem;
        border: none !important;
        text-align: left !important;
        padding: 4px 0px;
    }
    .sidebar-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .block-container {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "agno_agent" not in st.session_state:
    st.session_state.agno_agent = create_verne_agno_agent()

# --- Sidebar Controls ---
with st.sidebar:
    st.markdown("### 💼 Session Controls")
    if st.button("📈 Start New Chat"):
        if st.session_state.chat_history:
            st.session_state.all_chats[st.session_state.active_chat_id] = st.session_state.chat_history
        st.session_state.chat_history = []
        st.session_state.active_chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()

    if st.session_state.all_chats:
        st.markdown("### 🗂️ Chat History")
        for chat_id in sorted(st.session_state.all_chats.keys(), reverse=True):
            col1, col2 = st.columns([8, 2])
            with col1:
                if st.button(chat_id, key=f"load_{chat_id}"):
                    st.session_state.chat_history = st.session_state.all_chats[chat_id]
                    st.session_state.active_chat_id = chat_id
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    del st.session_state.all_chats[chat_id]
                    if chat_id == st.session_state.active_chat_id:
                        st.session_state.chat_history = []
                        st.session_state.active_chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.rerun()

# --- Initial Welcome Message ---
if not st.session_state.chat_history:
    welcome_message = """Welcome, founder 👋

I'm VerneBot — your personal coach for scaling and strategy.

Whether it's People, Strategy, Execution or Cash — I'm here to help you scale smart.

You can ask me:
• “How do I build a One-Page Strategic Plan?”
• “What are the Rockefeller Habits?”
• “How do I improve my cash conversion cycle?”

Let’s dive in.⚡"""
    st.session_state.chat_history.append(("assistant", welcome_message))

# --- Display Chat History ---
st.title("🚀 Chat with VerneBot")

for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)

# --- Chat Input + Response ---
prompt = st.chat_input("What challenge are we solving today?")

if prompt:
    st.session_state.chat_history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            kb_content, kb_score = get_knowledgebase_response(prompt)

            if kb_content and kb_score and kb_score > 0.7:
                response = get_response(prompt, st.session_state.chat_history)
                assistant_reply = f"\n\n{response.strip()}"
            else:
                agno_output = st.session_state.agno_agent.run(prompt)
                agno_clean = agno_output.content.strip() if hasattr(agno_output, "content") else str(agno_output)
                assistant_reply = f"\n\n{agno_clean}"

        except Exception as e:
            assistant_reply = f"⚠️ An error occurred: {e}"

        st.markdown(assistant_reply)
        st.session_state.chat_history.append(("assistant", assistant_reply))
