import streamlit as st
from utils.db import signup_user

def show_signup():
    st.title("📝 Sign Up")

    # Render the signup form
    with st.form("signup_form"):
        full_name = st.text_input("Full Name")
        nickname = st.text_input("Nickname")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign Up")

    # Handle submission
    if submitted:
        # ✅ Validate all fields
        if not full_name.strip() or not nickname.strip() or not email.strip() or not password.strip():
            st.error("❌ Please complete all fields before signing up.")
            return

        # Save user to database
        success = signup_user(full_name, nickname, email, password)

        if success:
            st.success("✅ Sign up successful! Redirecting to login...")

            # Switch to login page
            st.session_state["page"] = "login"

            # Streamlit new rerun function
            st.rerun()

        else:
            st.error("❌ Nickname or Email already exists.")
