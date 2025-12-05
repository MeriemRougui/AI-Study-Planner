import streamlit as st

def navigation_bar():
    st.markdown("""
        <style>
        .nav-container {
            display:flex;
            gap:10px;
            justify-content:center;
            background:#222;
            padding:10px;
            border-radius:6px;
            margin-bottom:20px;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("🏠 Home", key="nav_home"):
            st.session_state["page"] = "main"
            st.rerun()

    with col2:
        if st.button("🍅 Pomodoro", key="nav_pomodoro"):
            st.session_state["page"] = "pomodoro"
            st.rerun()

    with col3:
        if st.button("📊 Analytics", key="nav_analytics"):
            st.session_state["page"] = "analytics"
            st.rerun()

    with col4:
        if st.button("➕ Add Task", key="nav_add"):
            st.session_state["page"] = "add_task"
            st.rerun()

    with col5:
        if st.button("🚪 Logout", key="nav_logout"):
            st.session_state["user"] = None
            st.session_state["page"] = "login"
            st.rerun()
