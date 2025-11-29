import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db import get_tasks_for_user

def show_analytics():
    user = st.session_state.get("user")
    if not user:
        st.session_state["page"] = "login"
        st.rerun()

    st.title("📊 Productivity Analytics Dashboard")
    st.caption(f"Insights generated for {user['nickname']}")

    # Load tasks
    tasks = get_tasks_for_user(user["id"], completed_filter=None)

    if not tasks:
        st.info("Not enough data to generate analytics.")
        return

    df = pd.DataFrame(tasks)
    st.write("")  # spacing

    # --------------------------------------------
    # Load Focus Time (Pomodoro) Data
    # --------------------------------------------
    focus_time_df = pd.read_sql("""
        SELECT task_id, SUM(focus_time_minutes) as total_focus_time
        FROM task_focus_time
        GROUP BY task_id
    """, conn)  # Ensure to connect to MySQL

    # Merge focus time data with tasks
    df = df.merge(focus_time_df, left_on="id", right_on="task_id", how="left")

    # Display Focus Time in Analytics
    st.write("### 🕒 Task Focus Time (Pomodoro Sessions)")
    st.bar_chart(df.set_index("task_name")["total_focus_time"])

    st.write("---")

