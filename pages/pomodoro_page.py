import time
import streamlit as st
from utils.db import get_tasks_for_user, get_db_connection

# ==================================================
# DATABASE STATS - Total Focus Time & Sessions
# ==================================================
def get_total_focus(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*), SUM(focus_time_minutes)
        FROM task_focus_time
        WHERE task_id IN (SELECT id FROM tasks WHERE user_id = %s)
    """, (user_id,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    total_sessions = result[0] if result[0] else 0
    total_minutes = result[1] if result[1] else 0
    return total_sessions, total_minutes


# ==================================================
# MAIN POMODORO SCREEN
# ==================================================
def show_pomodoro():
    user = st.session_state.get("user")
    if not user:
        st.session_state["page"] = "login"
        st.rerun()

    # Load only unfinished tasks
    tasks = get_tasks_for_user(user["id"], completed_filter=0)
    if not tasks:
        st.info("You have no tasks to focus on!")
        return

    st.title("🍅 Pomodoro Focus Timer")

    # ----- Select Task -----
    task_list = [task["task_name"] for task in tasks]
    selected_task = st.selectbox("Choose a task to focus on:", task_list)
    selected_task_id = next(task["id"] for task in tasks if task["task_name"] == selected_task)

    # ----- Select Work Duration -----
    duration_choice = st.selectbox("Pomodoro duration (in minutes):", [25, 50, 90])
    break_length = 5  # fixed break for now

    # ====== TIMER STATE CONTROL ======
    if "pomodoro_duration" not in st.session_state:
        st.session_state.pomodoro_duration = duration_choice

    if "on_break" not in st.session_state:
        st.session_state.on_break = False  # Distinguish break vs work timer

    # Reset timer only when changing duration during an idle moment
    if duration_choice != st.session_state.pomodoro_duration and not st.session_state.on_break:
        st.session_state.pomodoro_duration = duration_choice
        st.session_state.pomodoro_time = duration_choice * 60

    if "pomodoro_time" not in st.session_state:
        st.session_state.pomodoro_time = duration_choice * 60

    if "pomodoro_running" not in st.session_state:
        st.session_state.pomodoro_running = False

    # Timer display
    minutes = st.session_state.pomodoro_time // 60
    seconds = st.session_state.pomodoro_time % 60

    if st.session_state.on_break:
        st.markdown(f"### 🧊 Break Time: **{minutes:02d}:{seconds:02d}**")
    else:
        st.markdown(f"### ⏳ Focus Session: **{minutes:02d}:{seconds:02d}**")

    # ----- Buttons -----
    col1, col2, col3 = st.columns(3)
    if col1.button("▶ Start"):
        st.session_state.pomodoro_running = True

    if col2.button("⏸ Pause"):
        st.session_state.pomodoro_running = False

    if col3.button("🔄 Reset"):
        st.session_state.pomodoro_running = False
        st.session_state.on_break = False
        st.session_state.pomodoro_time = st.session_state.pomodoro_duration * 60

    # ======== COUNTDOWN SYSTEM ========
    if st.session_state.pomodoro_running:
        time.sleep(1)
        st.session_state.pomodoro_time -= 1

        # 🔥 Focus Completed → Start Break
        if st.session_state.pomodoro_time <= 0 and not st.session_state.on_break:
            st.success("🎉 Focus Finished — Break Time Starts! 5 minutes 🧊")
            log_task_focus_time(selected_task_id, st.session_state.pomodoro_duration)

            st.session_state.on_break = True
            st.session_state.pomodoro_time = break_length * 60
            st.session_state.pomodoro_running = True
            st.rerun()

        # 🧊 Break Ended → Reset for new session
        elif st.session_state.pomodoro_time <= 0 and st.session_state.on_break:
            st.info("⏳ Break Over — Ready for another Pomodoro?")
            st.session_state.on_break = False
            st.session_state.pomodoro_time = st.session_state.pomodoro_duration * 60
            st.session_state.pomodoro_running = False
            st.rerun()

        st.rerun()

    # ==================================================
    # LIVE ANALYTICS
    # ==================================================
    st.write("---")
    st.subheader("📊 Productivity Stats")

    total_sessions, total_minutes = get_total_focus(user["id"])

    st.metric("Completed Focus Sessions", total_sessions)
    st.metric("Total Focus Minutes", f"{total_minutes} min")
    st.progress(min(float(total_minutes) / 300, 1.0))  # 300 min = 5-hour goal!


# ==================================================
# DB INSERT = Save Focus Session Time
# ==================================================
def log_task_focus_time(task_id, minutes):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO task_focus_time (task_id, focus_time_minutes)
        VALUES (%s, %s)
    """, (task_id, minutes))
    conn.commit()
    cursor.close()
    conn.close()
