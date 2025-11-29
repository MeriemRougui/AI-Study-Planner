# utils/train_model.py
import pandas as pd
import mysql.connector
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib
import warnings

warnings.filterwarnings("ignore")

def dump_and_train():
    # Connect to database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@meimei2002!",
        database="ai_study_planner"
    )

    # Load training data
    df = pd.read_sql("""
        SELECT difficulty, urgency, importance, duration, priority_score
        FROM tasks
        WHERE priority_score IS NOT NULL
    """, conn)
    conn.close()

    # Clean the data before training
    df = df.dropna()  # Remove rows with any missing values
    df = df[df['difficulty'] >= 0]  # Remove rows with invalid difficulty values
    df = df[df['urgency'] >= 0]  # Same for other columns
    df = df[df['importance'] >= 0]  # Ensure no invalid values in importance
    df = df[df['duration'] >= 0]  # Ensure no invalid values in duration

    # Check if there's enough data left after cleaning
    if df.shape[0] < 5:
        print("⚠️ Not enough valid data after cleaning. Using fallback dummy data.")
        df = pd.DataFrame({
            "difficulty": [1, 2, 3, 4, 5] * 5,
            "urgency":    [1, 2, 3, 4, 5] * 5,
            "importance": [1, 2, 3, 4, 5] * 5,
            "duration":   [1, 2, 3, 4, 5] * 5,
            "priority_score": [20, 40, 60, 80, 100] * 5
        })

    # Prepare data
    X = df[["difficulty", "urgency", "importance", "duration"]]
    y = df["priority_score"]

    # Check if the features and labels have no missing or invalid data
    assert not X.isnull().any().any(), "Features have missing values"
    assert not y.isnull().any(), "Labels have missing values"
    assert (y >= 0).all(), "Priority score has negative values"

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    try:
        # --------------------------
        # Train RandomForest
        # --------------------------
        rf = RandomForestRegressor(n_estimators=200, random_state=42)
        rf.fit(X_train, y_train)
        y_pred_rf = rf.predict(X_test)
        rf_score = r2_score(y_test, y_pred_rf)

        print(f"🌲 RandomForest R² Score: {rf_score:.4f}")

        # --------------------------
        # Train XGBoost
        # --------------------------
        xgb = XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42
        )
        xgb.fit(X_train, y_train)
        y_pred_xgb = xgb.predict(X_test)
        xgb_score = r2_score(y_test, y_pred_xgb)

        print(f"⚡ XGBoost R² Score: {xgb_score:.4f}")

        # --------------------------
        # Select the BEST model
        # --------------------------
        if xgb_score >= rf_score:
            best_model = xgb
            print("🏆 Best Model: XGBoost")
        else:
            best_model = rf
            print("🏆 Best Model: RandomForest")

        # Save the winning model
        joblib.dump(best_model, "models/priority_model.pkl")
        print("💾 Model saved → models/priority_model.pkl")

    except Exception as e:
        print("Error during model training:", e)

if __name__ == "__main__":
    dump_and_train()
