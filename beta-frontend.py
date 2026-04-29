import streamlit as st
import requests
import websocket
import asyncio

API_URL = "http://localhost:8000"

st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("messages", [])
st.session_state.setdefault("current_room", None)
st.session_state.setdefault("room_messages", [])
st.session_state.setdefault("roomID", [])
st.session_state.setdefault("token",None)
st.session_state.setdefault("ws",None)
st.session_state.setdefault("threadID",None)
# ─────────────────────────── AUTH ────────────────────────────

def login(username, password):
    res = requests.post(f"{API_URL}/user/login", json={"name": username, "password": password})
    
    jsonRes = res.json()
    
    if res.status_code == 200:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.token = jsonRes['token']
        st.session_state
        
        
        token = jsonRes['token']
        if st.session_state.ws is None:    
            ws = websocket.WebSocket()
            st.session_state.ws = ws
        else:
            ws = st.session_state.ws
            
        ws.connect("ws://localhost:8000", header={"Authorization": f"Bearer {token}"})
        
        
        st.rerun()
    else:
        st.error("Login failed.")

def signup(username, password, confirm):
    if password != confirm:
        st.error("Passwords do not match!")
        return
    res = requests.post(f"{API_URL}/user/signup", json={"name": username, "password": password})
    st.success("Signup successful! Please login.") if res.ok else st.error("Signup failed.")

def auth_page():
    st.title("🤖 RAG Chat Interface")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Login")
        u = st.text_input("Username", key="lu")
        p = st.text_input("Password", type="password", key="lp")
        if st.button("Login"):
            login(u, p)

    with col2:
        st.subheader("Signup")
        u = st.text_input("Username", key="su")
        p = st.text_input("Password", type="password", key="sp")
        c = st.text_input("Confirm Password", type="password", key="sc")
        if st.button("Sign Up"):
            signup(u, p, c)

# ─────────────────────────── ROOM HELPERS ────────────────────

def create_room():
    res = requests.post(f"{API_URL}/rooms/create", json={"created_by": st.session_state.username})
    
    if 1==1:
        st.session_state.current_room = res.json().get("room")
        st.session_state.room_messages = []
        st.rerun()
    else:
        st.error("Could not create room.")

def invite_friend(friend_username):
    if not friend_username.strip():
        st.error("Enter a username.")
        return
    if friend_username.strip() == st.session_state.username:
        st.error("You can't invite yourself.")
        return
    res = requests.post(f"{API_URL}/rooms/invite", json={
        "room_id": st.session_state.current_room["id"],
        "invited": friend_username.strip()
    })
    st.success(f"✅ Invited **{friend_username}**!") if res.ok else st.error("Could not invite user.")

def send_room_message(msg):
    res = requests.post(f"{API_URL}/rooms/message", json={
        "room_id": st.session_state.current_room["id"],
        "sender":  st.session_state.username,
        "message": msg
    })
    if res.ok:
        st.session_state.room_messages.append({"sender": st.session_state.username, "message": msg})
    else:
        st.error("Failed to send message.")

def fetch_room_messages():
    res = requests.get(f"{API_URL}/rooms/messages", params={"room_id": st.session_state.current_room["id"]})
    if res.ok:
        st.session_state.room_messages = res.json().get("messages", [])

# ─────────────────────────── CHAT PAGE ───────────────────────

def chat_page():

    # ── Left sidebar: config ─────────────────────────────────
    with st.sidebar:
        st.write(f"👤 **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.ws.close()
            for k in ["authenticated", "username", "messages", "current_room", "room_messages","ws"]:
                del st.session_state[k]
            st.rerun()

        st.divider()
        st.header("⚙️ Configuration")
        model = st.selectbox("Model", ["gpt-3.5-turbo", "deepseek-R1"])
        temp  = st.slider("Temperature", 0.0, 1.0, 0.7)

    # ── Main layout: chat | room panel ───────────────────────
    chat_col, room_col = st.columns([3, 1], gap="large")

    # ── RIGHT PANEL ──────────────────────────────────────────
    with room_col:

        # ── No room: just show Create button ─────────────────
        if not st.session_state.current_room:
            st.subheader("🏠 Room")
            st.caption("Start a room to chat with friends.")
            if st.button("➕ Create Room", use_container_width=True):
                create_room()

        # ── Room active: show chat panel ──────────────────────
        else:
            room = st.session_state.current_room
            members = room.get("members", [st.session_state.username])

            st.subheader("🏠 Room Chat")
            st.caption(f"👥 {', '.join(members)}")
            st.divider()

            # Invite friend
            with st.expander("➕ Invite Friend"):
                friend = st.text_input("Friend's username", key="invite_input", placeholder="e.g. john_doe")
                if st.button("Send Invite"):
                    invite_friend(friend)

            st.divider()

            # Room messages
            fetch_room_messages()
            msg_container = st.container(height=350)
            with msg_container:
                if st.session_state.room_messages:
                    for m in st.session_state.room_messages:
                        is_me = m["sender"] == st.session_state.username
                        align = "right" if is_me else "left"
                        name  = "You" if is_me else m["sender"]
                        st.markdown(
                            f"<div style='text-align:{align};margin-bottom:8px'>"
                            f"<small style='color:gray'>{name}</small><br>"
                            f"<span style='background:#f0f2f6;padding:4px 10px;border-radius:12px;display:inline-block'>"
                            f"{m['message']}</span></div>",
                            unsafe_allow_html=True
                        )
                else:
                    st.caption("No messages yet. Say hi! 👋")

            # Send message
            room_input = st.text_input("Message", key="room_msg_input", placeholder="Type a message...")
            if st.button("Send 💬", use_container_width=True):
                if room_input.strip():
                    send_room_message(room_input)
                    st.rerun()

            st.divider()
            if st.button("✖ Close Room", use_container_width=True):
                st.session_state.current_room = None
                st.session_state.room_messages = []
                st.rerun()

    # ── MAIN: RAG Chat ───────────────────────────────────────
    with chat_col:
        st.title("🤖 RAG Chat")

        with st.expander("📁 Upload Document"):
            file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"])
            if file and st.button("Upload to RAG"):
                res = requests.post(f"{API_URL}/rag/ingest", files={"file": file.getvalue()})
                st.success("Uploaded!") if res.ok else st.error("Upload failed.")

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Ask a question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            res = requests.post(f"{API_URL}/chat", json={
                "query": prompt,
                "temperature": temp,
                "username": st.session_state.username
            })
            answer = res.json().get("answer", "No response") if res.ok else "Error fetching response."

            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.chat_message("assistant").write(answer)

# ─────────────────────────── ROUTER ──────────────────────────

if not st.session_state.authenticated:
    auth_page()
else:
    chat_page()
