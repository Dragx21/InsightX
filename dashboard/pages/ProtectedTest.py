import streamlit as st
import requests

st.header("Protected Endpoint Test")
token = st.session_state.get("jwt_token", "")
if token:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://localhost:8000/protected", headers=headers)
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Access denied or not logged in.")
else:
    st.warning("Please log in first.")
