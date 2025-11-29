# app.py
import streamlit as st
from pages import login_page, signup_page, main_page, add_task_page
from pages import edit_task_page
from pages import analytics_page
from pages import pomodoro_page


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
        add_task_page.show_add_task()  # Ensure this matches the function name in add_task_page.py
    else:
        st.session_state["page"] = "login"
        st.rerun()

elif page == "edit_task":
    if st.session_state["user"]:
        edit_task_page.show_edit_task()
    else:
        st.session_state["page"] = "login"
        st.rerun()

elif st.session_state["page"] == "analytics":
    analytics_page.show_analytics()

elif st.session_state["page"] == "pomodoro":
    pomodoro_page.show_pomodoro()
