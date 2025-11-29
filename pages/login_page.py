# pages/login_page.py
import streamlit as st
from utils.db import login_user

def show_login():
    st.title("🔐 Login")

    identifier = st.text_input("Nickname or Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # ✅ Validate input fields
        if not identifier.strip() or not password.strip():
            st.error("❌ Please enter both your nickname/email and password.")
            return  # Stop here

        # Check credentials against MySQL database
        user = login_user(identifier, password)
        if user:
            st.session_state.user = user
            st.success(f"✅ Welcome, {user['nickname']}!")
            st.session_state.page = "main"  # Redirect to main page
        else:
            st.error("❌ Incorrect nickname/email or password.")

    st.write("---")
    if st.button("Sign Up"):
        st.session_state.page = "signup"  # Redirect to signup page
