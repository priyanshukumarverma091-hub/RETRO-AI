CREATE DATABASE IF NOT EXISTS multi_agent_db;

USE multi_agent_db;



CREATE TABLE IF NOT EXISTS chat_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL DEFAULT 'AI Assistant',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,

    session_id INT NOT NULL,

    role ENUM('user', 'ai', 'system') NOT NULL,

    content TEXT NOT NULL,

    agent VARCHAR(100) DEFAULT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES chat_sessions(id)
        ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS agent_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,

    session_id INT DEFAULT NULL,

    agent_name VARCHAR(100) NOT NULL,

    task TEXT,

    result TEXT,

    status ENUM('success', 'failed', 'running')
        DEFAULT 'success',

    execution_time_ms INT DEFAULT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES chat_sessions(id)
        ON DELETE SET NULL
);



CREATE TABLE IF NOT EXISTS system_config (
    id INT AUTO_INCREMENT PRIMARY KEY,

    config_key VARCHAR(100) UNIQUE NOT NULL,

    config_value TEXT,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);



INSERT INTO chat_sessions (title)
SELECT 'AI Assistant'
WHERE NOT EXISTS (
    SELECT 1
    FROM chat_sessions
    WHERE title = 'AI Assistant'
);