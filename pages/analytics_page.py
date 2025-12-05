import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db import get_tasks_for_user, get_db_connection 
from components.navbar import navigation_bar

def show_analytics():
    navigation_bar()
    user = st.session_state.get("user")
    if not user:
        st.session_state["page"] = "login"
        st.rerun()

    st.title("📊 Productivity Analytics Dashboard")
    st.caption(f"Insights generated for **{user['nickname']}**")

    # Load all tasks
    tasks = get_tasks_for_user(user["id"], completed_filter=None)
    if not tasks:
        st.info("Not enough data to generate analytics yet.")
        return

    df = pd.DataFrame(tasks)

    conn = get_db_connection() 
    focus_time_df = pd.read_sql("""
        SELECT task_id, SUM(focus_time_minutes) AS total_focus_time
        FROM task_focus_time
        GROUP BY task_id
    """, conn)
    conn.close()

    # Merge pomodoro tracking data into tasks
    df = df.merge(focus_time_df, left_on="id", right_on="task_id", how="left")
    df["total_focus_time"] = df["total_focus_time"].fillna(0)   # Replace NaN with 0

    # ========================= VISUALIZATION =========================
    st.subheader("🕒 Focus Time per Task (from Pomodoro Sessions)")
    st.bar_chart(df.set_index("task_name")["total_focus_time"])

    st.write("---")

    # Show table for transparency + future breakdown
    st.subheader("📄 Raw Stats Overview")
    st.dataframe(df[["task_name","due_date","difficulty","importance","urgency","total_focus_time"]])
