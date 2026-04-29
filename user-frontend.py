import streamlit as st
import requests
from streamlit_chat import message  # if you're using this package

api_url = "http://localhost:8000"

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "auth"
if "messages" not in st.session_state:
    st.session_state.messages = []

async def login_user(username, password):
    try:
        response = requests.post(
            f"{api_url}/user/login",
            json={"name": username, "password": password},
            timeout=10
        )
        response.raise_for_status()

        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.page = "rag"
        st.success("Login successful!")
        st.rerun()
        
        async with websockets.connect(uri) as websocket:
            await websocket.send("Hello Server")

            response = await websocket.recv()
            return response
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False

def signup_user(username, password, confirm_password):
    if password != confirm_password:
        st.error("Passwords do not match!")
        return False
    try:
        response = requests.post(
            f"{api_url}/user/signup",
            json={"name": username, "password": password},
            timeout=10
        )
        response.raise_for_status()
        st.success("Signup successful! Please login.")
        return True
    except Exception as e:
        st.error(f"Signup error: {str(e)}")
        return False

def render_auth_page():
    st.title("🤖 RAG Chat Interface")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            login_user(login_username, login_password)

    with col2:
        st.subheader("Signup")
        signup_username = st.text_input("Username", key="signup_user")
        signup_password = st.text_input("Password", type="password", key="signup_pass")
        signup_confirm = st.text_input("Confirm Password", type="password", key="signup_conf")
        if st.button("Sign Up"):
            signup_user(signup_username, signup_password, signup_confirm)

def render_rag_page():
    st.title("🤖 RAG Chat Interface")

    with st.sidebar:
        st.write(f"Logged in as: **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.page = "auth"
            st.session_state.messages = []
            st.rerun()

        st.header("Configuration")
        api_url_input = st.text_input("API URL", value=api_url)
        model_name = st.selectbox("Model", ["gpt-3.5-turbo", "deepseek-R1"])
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

    # File upload section
    with st.expander("📁 Upload Document"):
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"])
        if uploaded_file is not None:
            if st.button("Upload to RAG"):
                try:
                    files = {"file": uploaded_file.getvalue()}
                    response = requests.post(
                        f"{api_url_input}/rag/ingest",
                        files=files,
                        timeout=30
                    )
                    response.raise_for_status()
                    st.success("File uploaded successfully!")
                except Exception as e:
                    st.error(f"Upload error: {str(e)}")

    # Display chat history
    for i, msg in enumerate(st.session_state.messages):
        message(msg["content"], is_user=msg["role"] == "user", key=str(i))

    # Chat input
    user_input = st.chat_input("Ask a question...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        message(user_input, is_user=True)

        try:
            response = requests.post(
                f"{api_url_input}/chat",
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

# Route to the correct page
if not st.session_state.authenticated or st.session_state.page == "auth":
    render_auth_page()
else:
    render_rag_page()