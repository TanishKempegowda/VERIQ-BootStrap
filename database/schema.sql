-- database/schema.sql

CREATE TABLE IF NOT EXISTS audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_name TEXT NOT NULL,
    audit_type TEXT NOT NULL, -- 'Compliance' or 'Operational'
    department TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_id INTEGER,
    issue_description TEXT NOT NULL,
    severity TEXT NOT NULL, -- 'High', 'Medium', 'Low'
    evidence TEXT,
    status TEXT DEFAULT 'Open', -- 'Open', 'Resolved', 'Recurring'
    FOREIGN KEY(audit_id) REFERENCES audits(id)
);

CREATE TABLE IF NOT EXISTS corrective_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    finding_id INTEGER,
    assigned_to TEXT,
    action_description TEXT,
    due_date DATE,
    is_verified BOOLEAN DEFAULT 0,
    FOREIGN KEY(finding_id) REFERENCES findings(id)
);
CREATE TABLE IF NOT EXISTS policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_name TEXT NOT NULL,
    extracted_requirements TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
