import streamlit as st
import requests

st.header("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_btn = st.button("Login")

if login_btn:
    response = requests.post(
        "http://localhost:8000/token",
        data={"username": username, "password": password}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        st.session_state["jwt_token"] = token
        st.success("Login successful!")
    else:
        st.error("Invalid username or password.")
    