# app.py
import streamlit as st
from pages import login_page, signup_page, main_page, add_task_page
from pages import edit_task_page, analytics_page, pomodoro_page
from pages.ai_assistant import show_ai_assistant

# -----------------------------
# Initialize session state
# -----------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "user" not in st.session_state:
    st.session_state["user"] = None

# -----------------------------
# Page Routing
# -----------------------------
page = st.session_state["page"]

if page == "login":
    login_page.show_login()

elif page == "signup":
    signup_page.show_signup()

elif page == "main":
    if st.session_state["user"]:
        main_page.show_main()
    else:
        st.session_state["page"] = "login"
        st.rerun()

elif page == "add_task":
    if st.session_state["user"]:
        add_task_page.show_add_task()
    else:
        st.session_state["page"] = "login"
        st.rerun()

elif page == "edit_task":
    if st.session_state["user"]:
        edit_task_page.show_edit_task()
    else:
        st.session_state["page"] = "login"
        st.rerun()

elif page == "analytics":  # Fixed: use page variable consistently
    if st.session_state["user"]:
        analytics_page.show_analytics()
    else:
        st.session_state["page"] = "login"
        st.rerun()

elif page == "pomodoro":  # Fixed: use page variable consistently
    if st.session_state["user"]:
        pomodoro_page.show_pomodoro()
    else:
        st.session_state["page"] = "login"
        st.rerun()

elif page == "ai_assistant":
    if st.session_state["user"]:  # Added authentication check
        show_ai_assistant()
    else:
        st.session_state["page"] = "login"
        st.rerun()

# Add a catch-all for unknown pages
else:
    st.error(f"Unknown page: {page}")
    st.session_state["page"] = "login"
    st.rerun()