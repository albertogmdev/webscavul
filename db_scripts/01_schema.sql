USE webscavul;

-- Tables
DROP TABLE IF EXISTS Report;
DROP TABLE IF EXISTS List;
DROP TABLE IF EXISTS Task;

-- Create Schema
CREATE TABLE Report (
    id VARCHAR(255) PRIMARY KEY,
    type VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    domain VARCHAR(255) NOT NULL,
    full_domain VARCHAR(255) NOT NULL,
    protocol VARCHAR(6) NOT NULL,
    ip JSON,
    alias JSON,
    server VARCHAR(255),
    powered VARCHAR(255),
    generator VARCHAR(255),
    vulnerabilities INT,
    port INT,
    ssl_info JSON,
    hsts JSON,
    csp JSON,
    xframe JSON,
    content_type JSON,
    cookie JSON,
    cache JSON,
    xss JSON,
    referrer JSON,
    permissions JSON,
    refresh JSON
);

-- Create List
CREATE TABLE List (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    archived BOOLEAN NOT NULL,
    FOREIGN KEY (report_id) REFERENCES Report(id)
        ON DELETE CASCADE
);

-- Create Task
CREATE TABLE Task (
    id INT AUTO_INCREMENT PRIMARY KEY,
    list_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(10) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    location VARCHAR(255),
    code TEXT,
    details VARCHAR(512),
    status INT NOT NULL,
    archived BOOLEAN NOT NULL,
    FOREIGN KEY (list_id) REFERENCES List(id)
        ON DELETE CASCADE
);