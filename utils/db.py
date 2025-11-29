# utils/db.py
import mysql.connector
import hashlib
from dotenv import load_dotenv
import os
from utils.ml_model import predict_priority

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
    return conn

# -----------------------------
# Password hashing
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -----------------------------
# User functions
# -----------------------------
def login_user(identifier, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    hashed_pw = hash_password(password)
    query = "SELECT * FROM users WHERE (nickname=%s OR email=%s) AND password=%s"
    cursor.execute(query, (identifier, identifier, hashed_pw))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def signup_user(full_name, nickname, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        cursor.execute("""
            INSERT INTO users (full_name, nickname, email, password)
            VALUES (%s, %s, %s, %s)
        """, (full_name, nickname, email, hashed_pw))
        conn.commit()
        return True
    except mysql.connector.errors.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()

# -----------------------------
# Task functions
# -----------------------------
def get_tasks_for_user(user_id, completed_filter=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, task_name, due_date, difficulty, urgency, importance,
               duration, priority_score, ai_tip, completed
        FROM tasks
        WHERE user_id = %s
    """

    params = [user_id]

    if completed_filter is not None:
        query += " AND completed = %s"
        params.append(completed_filter)

    query += " ORDER BY due_date ASC"

    cursor.execute(query, params)
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()
    return tasks

def add_task(user_id, task_name, due_date, difficulty, urgency, importance, duration, ai_tip):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        priority_score = predict_priority(difficulty, urgency, importance, duration)
        cursor.execute("""
            INSERT INTO tasks
            (user_id, task_name, due_date, difficulty, urgency, importance,
             duration, priority_score, ai_tip)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, task_name, due_date, difficulty, urgency, importance, duration,
              priority_score, ai_tip))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("add_task error:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("delete_task error:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def update_task_with_priority(task_id, task_name, due_date, difficulty, urgency, importance, duration, priority_score, ai_tip):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE tasks
            SET task_name=%s,
                due_date=%s,
                difficulty=%s,
                urgency=%s,
                importance=%s,
                duration=%s,
                priority_score=%s,
                ai_tip=%s
            WHERE id=%s
        """, (task_name, due_date, difficulty, urgency, importance,
              duration, priority_score, ai_tip, task_id))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("update_task_with_priority ERROR:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def update_task_completion(task_id, completed):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tasks SET completed = %s WHERE id = %s", (completed, task_id))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("update_task_completion error:", e)
        return False
    finally:
        cursor.close()
        conn.close()
