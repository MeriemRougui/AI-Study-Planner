import streamlit as st
from utils.db import add_task
from components.navbar import navigation_bar

def show_add_task():
    navigation_bar()
    st.title("➕ Add New Task")

    user = st.session_state.get("user")
    if not user:
        st.session_state["page"] = "login"
        st.rerun()

    # Task form
    with st.form(key='add_task_form'):
        task_name = st.text_input("Task Name")
        due_date = st.date_input("Due Date")
        difficulty = st.slider("Difficulty", 1, 5)
        urgency = st.slider("Urgency", 1, 5)
        importance = st.slider("Importance", 1, 5)
        ai_tip = st.text_area("AI Tip (optional)")

        submit_button = st.form_submit_button(label="Add Task")

    # Add task to the database
    if submit_button:
        if not task_name or not due_date:  # Ensure fields are filled
            st.error("❌ Please fill out all required fields.")
        else:
            success = add_task(user["id"], task_name, due_date, difficulty, urgency, importance, duration, ai_tip)
            if success:
                st.success("✅ Task added successfully!")
                st.session_state["page"] = "main"
                st.rerun()  # Refresh to go back to main page after adding task
            else:
                st.error("❌ Failed to add task. Please try again.")

    st.write("---")
    if st.button("Back to Main Page"):
        st.session_state["page"] = "main"
        st.rerun()
