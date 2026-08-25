import json
import streamlit as st

from db import (
    init_db,
    get_students,
    get_student,
    get_prediction,
    get_shap,
    get_interventions,
    get_reassessment,
    get_latest_decision,
    save_decision,
)
from advisor_agent import ask_advisor_agent

st.set_page_config(page_title="Student Success Advisor Agent", layout="wide")
init_db()

st.sidebar.title("Student Success Advisor Agent")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Student Review", "Advisor Assistant"]
)

# ---------------- Dashboard ----------------
if page == "Dashboard":
    st.title("Dashboard")
    st.caption("Simple advisor view of the frozen Week 5 risk results.")

    students = get_students()

    if not students:
        st.warning("No demo data found. Run: python seed_demo.py")
        st.stop()

    total = len(students)
    at_risk = sum(int(x["predicted_label"]) for x in students)
    pending = sum(x["review_status"] == "Pending" for x in students)

    c1, c2, c3 = st.columns(3)
    c1.metric("Students", total)
    c2.metric("At risk", at_risk)
    c3.metric("Pending review", pending)

    risk_filter = st.selectbox("Show", ["At risk only", "All students"])

    rows = students
    if risk_filter == "At risk only":
        rows = [x for x in rows if int(x["predicted_label"]) == 1]

    st.dataframe(
        [
            {
                "Student": x["student_key"],
                "Programme": x["programme_or_school"],
                "Year": x["year_level"],
                "Risk": f'{x["risk_probability"]:.1%}',
                "Status": "At risk" if x["predicted_label"] else "Not at risk",
                "Review": x["review_status"],
            }
            for x in rows
        ],
        use_container_width=True,
        hide_index=True,
    )

    selected = st.selectbox("Open student", [x["student_key"] for x in rows])
    if st.button("Review student", type="primary"):
        st.session_state["student_key"] = selected
        st.session_state["page"] = "Student Review"
        st.rerun()


# ---------------- Student Review ----------------
elif page == "Student Review":
    st.title("Student Review")
    st.caption("The advisor reviews the evidence and saves the final human decision.")

    students = get_students()
    keys = [x["student_key"] for x in students]

    default_key = st.session_state.get("student_key", keys[0])
    default_index = keys.index(default_key) if default_key in keys else 0
    student_key = st.selectbox("Student", keys, index=default_index)
    st.session_state["student_key"] = student_key

    student = get_student(student_key)
    prediction = get_prediction(student_key)
    shap = get_shap(student_key)
    interventions = get_interventions(student_key)
    reassessment = get_reassessment(student_key)
    latest = get_latest_decision(student_key)

    c1, c2, c3 = st.columns(3)
    c1.metric("Risk probability", f'{prediction["risk_probability"]:.1%}')
    c2.metric("Prediction", "At risk" if prediction["predicted_label"] else "Not at risk")
    c3.metric("Review", latest["review_status"] if latest else "Pending")

    st.markdown("### Student snapshot")
    st.write(
        f'**Programme:** {student["programme_or_school"]}  \n'
        f'**Year:** {student["year_level"]}  \n'
        f'**Attendance:** {student["attendance_rate"]:.1%}  \n'
        f'**Course access rate:** {student["course_access_rate"]:.1%}  \n'
        f'**Active days rate:** {student["active_days_rate"]:.1%}'
    )

    st.markdown("### Why was this student flagged?")
    if shap:
        st.dataframe(
            [
                {
                    "Factor": x["feature_name"],
                    "Value": x["feature_value"],
                    "Effect": "Increases risk" if x["shap_value"] > 0 else "Reduces risk",
                }
                for x in shap[:5]
            ],
            use_container_width=True,
            hide_index=True,
        )
        st.caption("SHAP explains the model prediction. It does not prove causality.")

    st.markdown("### Proposed support")
    if interventions:
        for x in interventions:
            st.write(f'**{x["intervention_type"]}:** {x["proposed_action"]}')
    else:
        st.info("No intervention is proposed for this student.")

    st.markdown("### Reassessment")
    if reassessment:
        st.dataframe(
            [
                {
                    "Scenario": x["scenario"],
                    "Baseline risk": f'{x["baseline_risk"]:.1%}',
                    "Reassessed risk": f'{x["mean_reassessed_risk"]:.1%}',
                    "Risk reduction": f'{x["mean_risk_reduction"]:.1%}',
                }
                for x in reassessment
            ],
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "These are stored synthetic scenario estimates from the thesis pipeline, "
            "not observed intervention outcomes."
        )

    st.markdown("### Advisor decision")

    intervention_names = [x["intervention_type"] for x in interventions]
    with st.form("decision_form"):
        decision = st.selectbox(
            "Decision",
            ["Approve", "Modify", "No intervention", "Further review"]
        )
        selected_support = st.multiselect(
            "Selected support",
            intervention_names,
            default=intervention_names if decision == "Approve" else []
        )
        notes = st.text_area("Advisor notes")
        review_status = st.selectbox(
            "Review status",
            ["Pending", "Completed"]
        )

        if st.form_submit_button("Save decision", type="primary"):
            save_decision(
                student_key,
                decision,
                selected_support,
                notes,
                review_status,
            )
            st.success("Human advisor decision saved.")
            st.rerun()


# ---------------- Advisor Assistant ----------------
else:
    st.title("Advisor Assistant")
    st.caption(
        "One read-only assistant that explains the stored student evidence. "
        "It cannot save decisions."
    )

    students = get_students()
    keys = [x["student_key"] for x in students]
    student_key = st.selectbox(
        "Student",
        keys,
        index=keys.index(st.session_state.get("student_key", keys[0]))
        if st.session_state.get("student_key", keys[0]) in keys else 0,
    )
    st.session_state["student_key"] = student_key

    quick = st.radio(
        "Quick question",
        [
            "Summarise this student",
            "Why is this student at risk?",
            "What support is proposed?",
            "What does the reassessment show?",
        ],
    )

    custom = st.text_input("Or ask your own question")
    question = custom.strip() or quick

    if st.button("Ask assistant", type="primary"):
        with st.spinner("Reading the stored evidence..."):
            answer = ask_advisor_agent(student_key, question)
        st.markdown(answer)

    st.info(
        "The assistant is read-only. It does not run SQL directly, change the risk model, "
        "write advisor decisions, or use a policy tool."
    )
