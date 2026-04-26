import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(page_title="RAG Chat", layout="wide")

st.title("🤖 RAG Chat Interface")

api_url = 'http://127.0.0.1:8000'

# File upload section
with st.expander("📁 Upload Document"):
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"])
    if uploaded_file is not None:
        if st.button("Upload to RAG"):
            try:
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(
                    f"{api_url}/rag/ingest",
                    files=files,
                    timeout=30
                )
                response.raise_for_status()
                st.success("File uploaded successfully!")
            except Exception as e:
                st.error(f"Upload error: {str(e)}")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_url = st.text_input("API URL", value="http://localhost:8000")
    model_name = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=str(i))

# Chat input
user_input = st.chat_input("Ask a question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True)
    
    # Call RAG backend
    try:
        response = requests.post(
            f"{api_url}/chat",
            json={"query": user_input, "temperature": temperature},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        assistant_response = result.get("answer", "No response")
        
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        message(assistant_response, is_user=False)
    except Exception as e:
        st.error(f"Error: {str(e)}")