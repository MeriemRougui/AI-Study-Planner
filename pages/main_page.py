import streamlit as st
import numpy as np
import joblib
from utils.db import (
    get_tasks_for_user,
    delete_task,
    update_task_completion
)

# -------------------------------------------------------
# AI RECOMMENDATION FUNCTION
# -------------------------------------------------------
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


# -------------------------------------------------------
# MAIN PAGE
# -------------------------------------------------------
def show_main():
    user = st.session_state.get("user")
    if not user:
        st.session_state["page"] = "login"
        st.rerun()

    st.title("📚 AI Study Planner")
    st.subheader(f"Welcome back, **{user['nickname']}** 👋")

    st.write("---")

    # -------------------------------------------------------
    # AI RECOMMENDATION SECTION
    # -------------------------------------------------------
    st.subheader("🤖 AI Assistant")

    if "ask_ai" not in st.session_state:
        st.session_state["ask_ai"] = False

    if st.button("🔥 What Should I Do Next?"):
        st.session_state["ask_ai"] = True
        st.rerun()

    if st.session_state["ask_ai"]:
        show_ai_recommendation(user["id"])

    st.write("---")

    # -------------------------------------------------------
    # FILTER BUTTONS (Done / Undone)
    # -------------------------------------------------------
    if "task_filter" not in st.session_state:
        st.session_state["task_filter"] = 0  # default = show undone

    st.subheader("Filter Tasks")

    colA, colB = st.columns(2)

    with colA:
        if st.button("📌 UNDONE Tasks"):
            st.session_state["task_filter"] = 0
            st.session_state["ask_ai"] = False
            st.rerun()

    with colB:
        if st.button("✔ DONE Tasks"):
            st.session_state["task_filter"] = 1
            st.session_state["ask_ai"] = False
            st.rerun()

    st.write("---")

    # Load tasks based on filter
    tasks = get_tasks_for_user(user["id"], st.session_state["task_filter"])

    st.header("📝 Your Tasks")

    if not tasks:
        st.info("No tasks found for this category.")
    else:
        for task in tasks:
            col1, col2, col3 = st.columns([4, 1, 1])

            # ------------------------------------------
            # ✔ COMPLETION CHECKBOX
            # ------------------------------------------
            with col1:
                is_done = st.checkbox(
                    f"{task['task_name']} – {task['due_date']}",
                    value=bool(task["completed"]),
                    key=f"done_{task['id']}"
                )

                if is_done != bool(task["completed"]):
                    update_task_completion(task["id"], int(is_done))
                    st.session_state["ask_ai"] = False
                    st.rerun()

            # ------------------------------------------
            # ✏ EDIT BUTTON
            # ------------------------------------------
            with col2:
                if st.button("✏️", key=f"edit_{task['id']}"):
                    st.session_state["task_to_edit"] = task
                    st.session_state["ask_ai"] = False
                    st.session_state["page"] = "edit_task"
                    st.rerun()

            # ------------------------------------------
            # ❌ DELETE BUTTON
            # ------------------------------------------
            with col3:
                if st.button("❌", key=f"delete_{task['id']}"):
                    delete_task(task["id"])
                    st.session_state["ask_ai"] = False
                    st.rerun()

    st.write("---")

    # -------------------------------------------------------
    # Bottom Buttons (Add Task / Pomodoro / Analytics / Logout)
    # -------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("➕ Add New Task"):
            st.session_state["page"] = "add_task"
            st.rerun()

    with col2:
        if st.button("🍅 Pomodoro"):
            st.session_state["page"] = "pomodoro"
            st.rerun()

    with col3:
        if st.button("📊 Analytics"):
            st.session_state["page"] = "analytics"
            st.rerun()

    with col4:
        if st.button("🚪 Logout"):
            st.session_state["user"] = None
            st.session_state["page"] = "login"
            st.rerun()
