import streamlit as st
import numpy as np
import joblib
from utils.db import (
    get_tasks_for_user,
    delete_task,
    update_task_completion
)

def navigation_bar():
    st.markdown(
        """
        <style>
        .topnav {
            background-color: #111827;
            overflow: hidden;
            padding: 10px;
            border-radius: 8px;
        }
        .topnav a {
            float: left;
            color: white;
            text-align: center;
            padding: 10px 18px;
            text-decoration: none;
            font-size: 17px;
            font-weight: 600;
        }
        .topnav a:hover {
            background-color: #4F46E5;
            border-radius:6px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("🏠 Home", key="nav_home"):
            st.session_state["page"] = "main"
            st.rerun()

    with col2:
        if st.button("➕ Add Task", key="nav_add"):
            st.session_state["page"] = "add_task"
            st.rerun()

    with col3:
        if st.button("🍅 Pomodoro", key="nav_pomo"):
            st.session_state["page"] = "pomodoro"
            st.rerun()

    with col4:
        if st.button("📊 Analytics", key="nav_analytics"):
            st.session_state["page"] = "analytics"
            st.rerun()

    with col5:
        if st.button("🤖 Study AI", key="nav_ai"):
            st.session_state["page"] = "ai_assistant"
            st.rerun()


def show_ai_recommendation(user_id):
    model = joblib.load("models/priority_model.pkl")

    # Load only undone tasks
    tasks = get_tasks_for_user(user_id, completed_filter=0)

    if not tasks:
        st.info("You have no pending tasks!")
        return

    best_task = None
    best_score = -999

    for task in tasks:
        features = np.array([[task["difficulty"], task["urgency"], task["importance"], task["duration"]]])
        score = float(model.predict(features)[0])

        if score > best_score:
            best_score = score
            best_task = task

    # Display best recommendation
    st.success("🎯 Recommended Task to Do Next:")
    st.markdown(f"""
        ### 📘 **{best_task['task_name']}**

        **🔥 Priority Score:** `{int(best_score)}`  
        **⏳ Due:** `{best_task['due_date']}`  
        **⭐ Difficulty:** {best_task['difficulty']}  
        **⚡ Urgency:** {best_task['urgency']}  
        **🎯 Importance:** {best_task['importance']}  
        **⏱ Duration:** {best_task['duration']} hours  
    """)

def show_main():
    navigation_bar()

    user = st.session_state.get("user")
    if not user:
        st.session_state["page"] = "login"
        st.rerun()

    st.title("📚 AI Study Planner")
    st.write(f"Welcome back, **{user['nickname']}** 👋")
    st.write("---")

    # ================= AI Recommendation ==================
    st.subheader("🤖 AI Assistant")

    if "ask_ai" not in st.session_state:
        st.session_state.ask_ai = False

    if st.button("🔥 What Should I Do Next?"):
        st.session_state.ask_ai = True
        st.rerun()

    if st.session_state.ask_ai:
        show_ai_recommendation(user["id"])

    st.write("---")

    # ================= Filter Tasks =======================
    if "task_filter" not in st.session_state:
        st.session_state.task_filter = 0

    st.subheader("Filter Tasks")
    colA, colB = st.columns(2)

    if colA.button("📌 Show UNDONE"):
        st.session_state.task_filter = 0
        st.rerun()

    if colB.button("✔ Show DONE"):
        st.session_state.task_filter = 1
        st.rerun()

    st.write("---")

    # ================= Tasks List =========================
    st.header("📝 Your Tasks")
    tasks = get_tasks_for_user(user["id"], st.session_state.task_filter)

    if not tasks:
        st.info("No tasks here yet.")
        return

    for task in tasks:
        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            is_done = st.checkbox(
                f"{task['task_name']} – {task['due_date']}",
                value=bool(task["completed"]),
                key=f"done_{task['id']}"
            )
            if is_done != bool(task["completed"]):
                update_task_completion(task["id"], int(is_done))
                st.rerun()

        if col2.button("✏️", key=f"edit_{task['id']}"):
            st.session_state["task_to_edit"] = task
            st.session_state["page"] = "edit_task"
            st.rerun()

        if col3.button("❌", key=f"delete_{task['id']}"):
            delete_task(task["id"])
            st.rerun()
