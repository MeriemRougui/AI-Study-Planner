import streamlit as st
import joblib
import numpy as np
from utils.db import update_task_with_priority

def show_edit_task():
    user = st.session_state.get("user")
    if not user:
        st.session_state["page"] = "login"
        st.rerun()

    task = st.session_state.get("task_to_edit")

    if not task:
        st.error("No task selected for editing.")
        st.session_state["page"] = "main"
        st.rerun()

    st.title("✏️ Edit Task")

    with st.form(key="edit_task_form"):
        task_name = st.text_input("Task Name", value=task["task_name"])
        due_date = st.date_input("Due Date", value=task["due_date"])
        difficulty = st.slider("Difficulty", 1, 5, value=task["difficulty"])
        urgency = st.slider("Urgency", 1, 5, value=task["urgency"])
        importance = st.slider("Importance", 1, 5, value=task["importance"])
        duration = st.slider("Duration (hours)", 1, 12, value=task["duration"])
        ai_tip = st.text_area("AI Tip (optional)", value=task["ai_tip"])

        submit_btn = st.form_submit_button("Update Task")

    if submit_btn:
        # Load the ML model
        model = joblib.load("models/priority_model.pkl")

        # Prepare data for prediction
        features = np.array([[difficulty, urgency, importance, duration]])

        # Predict new priority score
        new_priority_score = int(model.predict(features)[0])

        # Update task in DB
        success = update_task_with_priority(
            task["id"], task_name, due_date, difficulty,
            urgency, importance, duration,
            new_priority_score, ai_tip
        )

        if success:
            st.success(f"✅ Task updated! New priority score: {new_priority_score}")
            st.session_state["page"] = "main"
            st.rerun()
        else:
            st.error("❌ Failed to update task.")

    if st.button("⬅ Back"):
        st.session_state["page"] = "main"
        st.rerun()
