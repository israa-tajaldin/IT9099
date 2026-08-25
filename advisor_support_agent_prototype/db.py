import json
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "data" / "prototype.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    student_key TEXT PRIMARY KEY,
    programme_or_school TEXT,
    year_level INTEGER,
    attendance_rate REAL,
    course_access_rate REAL,
    active_days_rate REAL
);

CREATE TABLE IF NOT EXISTS predictions (
    student_key TEXT PRIMARY KEY,
    risk_probability REAL,
    predicted_label INTEGER,
    FOREIGN KEY(student_key) REFERENCES students(student_key)
);

CREATE TABLE IF NOT EXISTS shap_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_key TEXT,
    feature_name TEXT,
    feature_value TEXT,
    shap_value REAL,
    FOREIGN KEY(student_key) REFERENCES students(student_key)
);

CREATE TABLE IF NOT EXISTS interventions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_key TEXT,
    intervention_type TEXT,
    proposed_action TEXT,
    FOREIGN KEY(student_key) REFERENCES students(student_key)
);

CREATE TABLE IF NOT EXISTS reassessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_key TEXT,
    scenario TEXT,
    baseline_risk REAL,
    mean_reassessed_risk REAL,
    mean_risk_reduction REAL,
    FOREIGN KEY(student_key) REFERENCES students(student_key)
);

CREATE TABLE IF NOT EXISTS mentor_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_key TEXT,
    decision TEXT,
    selected_support TEXT,
    advisor_notes TEXT,
    review_status TEXT,
    created_at TEXT
);
"""

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    with connect() as conn:
        conn.executescript(SCHEMA)

def get_students():
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT s.student_key, s.programme_or_school, s.year_level,
                   p.risk_probability, p.predicted_label,
                   COALESCE(
                       (SELECT review_status
                        FROM mentor_decisions m
                        WHERE m.student_key=s.student_key
                        ORDER BY id DESC LIMIT 1),
                       'Pending'
                   ) AS review_status
            FROM students s
            JOIN predictions p ON p.student_key=s.student_key
            ORDER BY p.risk_probability DESC
            """
        ).fetchall()
    return [dict(x) for x in rows]

def get_student(student_key):
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE student_key=?",
            (student_key,)
        ).fetchone()
    return dict(row) if row else None

def get_prediction(student_key):
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM predictions WHERE student_key=?",
            (student_key,)
        ).fetchone()
    return dict(row) if row else None

def get_shap(student_key):
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT feature_name, feature_value, shap_value
            FROM shap_values
            WHERE student_key=?
            ORDER BY ABS(shap_value) DESC
            """,
            (student_key,)
        ).fetchall()
    return [dict(x) for x in rows]

def get_interventions(student_key):
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT intervention_type, proposed_action
            FROM interventions
            WHERE student_key=?
            ORDER BY id
            """,
            (student_key,)
        ).fetchall()
    return [dict(x) for x in rows]

def get_reassessment(student_key):
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT scenario, baseline_risk, mean_reassessed_risk, mean_risk_reduction
            FROM reassessments
            WHERE student_key=?
            ORDER BY CASE scenario
                WHEN 'Conservative' THEN 1
                WHEN 'Moderate' THEN 2
                WHEN 'Strong' THEN 3
                ELSE 4
            END
            """,
            (student_key,)
        ).fetchall()
    return [dict(x) for x in rows]

def get_latest_decision(student_key):
    with connect() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM mentor_decisions
            WHERE student_key=?
            ORDER BY id DESC
            LIMIT 1
            """,
            (student_key,)
        ).fetchone()
    return dict(row) if row else None

def save_decision(student_key, decision, selected_support, notes, review_status):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO mentor_decisions
            (student_key, decision, selected_support, advisor_notes, review_status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student_key,
                decision,
                json.dumps(selected_support),
                notes,
                review_status,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
