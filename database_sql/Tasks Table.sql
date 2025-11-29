CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    due_date DATE NOT NULL,
    difficulty INT NOT NULL,
    urgency INT NOT NULL,
    importance INT NOT NULL,
    duration INT NOT NULL,
    priority_score INT NOT NULL,
    ai_tip VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

USE ai_study_planner;
ALTER TABLE tasks 
ADD COLUMN completed TINYINT(1) DEFAULT 0;
