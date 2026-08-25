from db import init_db, connect, DB_PATH
import random

if DB_PATH.exists():
    DB_PATH.unlink()

init_db()
random.seed(7)

with connect() as conn:
    for i in range(1, 11):
        key = f"STU-{i:03d}"
        attendance = round(random.uniform(0.55, 0.95), 2)
        access = round(random.uniform(0.45, 0.95), 2)
        active = round(random.uniform(0.40, 0.90), 2)

        risk = round(
            min(
                0.92,
                max(
                    0.18,
                    0.25
                    + (1-attendance)*0.70
                    + (1-access)*0.35
                    + (1-active)*0.35
                ),
            ),
            3,
        )
        label = int(risk >= 0.50)

        conn.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
            (
                key,
                ["ICT", "Business", "Engineering"][i % 3],
                (i % 4) + 1,
                attendance,
                access,
                active,
            ),
        )
        conn.execute(
            "INSERT INTO predictions VALUES (?, ?, ?)",
            (key, risk, label),
        )

        effects = [
            ("attendance_rate", attendance, 0.75-attendance),
            ("course_access_rate", access, 0.70-access),
            ("active_days_rate", active, 0.65-active),
        ]
        for name, value, effect in effects:
            conn.execute(
                """
                INSERT INTO shap_values
                (student_key, feature_name, feature_value, shap_value)
                VALUES (?, ?, ?, ?)
                """,
                (key, name, str(value), effect),
            )

        if label:
            if attendance < 0.75:
                conn.execute(
                    """
                    INSERT INTO interventions
                    (student_key, intervention_type, proposed_action)
                    VALUES (?, ?, ?)
                    """,
                    (
                        key,
                        "Attendance support",
                        "Agree a short attendance improvement plan and follow-up.",
                    ),
                )

            if access < 0.70 or active < 0.65:
                conn.execute(
                    """
                    INSERT INTO interventions
                    (student_key, intervention_type, proposed_action)
                    VALUES (?, ?, ?)
                    """,
                    (
                        key,
                        "Engagement support",
                        "Agree a weekly Moodle engagement target and advisor check-in.",
                    ),
                )

            reductions = {
                "Conservative": 0.03,
                "Moderate": 0.09,
                "Strong": 0.15,
            }
            for scenario, reduction in reductions.items():
                conn.execute(
                    """
                    INSERT INTO reassessments
                    (student_key, scenario, baseline_risk,
                     mean_reassessed_risk, mean_risk_reduction)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        key,
                        scenario,
                        risk,
                        max(0.05, risk-reduction),
                        reduction,
                    ),
                )

print("Simple synthetic demo database created.")
