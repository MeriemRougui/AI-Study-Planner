USE ai_study_planner;
CREATE TABLE task_focus_time (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    focus_time_minutes INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
