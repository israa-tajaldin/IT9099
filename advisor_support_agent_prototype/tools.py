from db import (
    get_student,
    get_prediction,
    get_shap,
    get_interventions,
    get_reassessment,
)

def student_profile_tool(student_key):
    return get_student(student_key)

def risk_tool(student_key):
    return get_prediction(student_key)

def shap_tool(student_key):
    return get_shap(student_key)

def intervention_tool(student_key):
    return get_interventions(student_key)

def reassessment_tool(student_key):
    return get_reassessment(student_key)

def get_context(student_key):
    return {
        "profile": student_profile_tool(student_key),
        "prediction": risk_tool(student_key),
        "shap": shap_tool(student_key),
        "interventions": intervention_tool(student_key),
        "reassessment": reassessment_tool(student_key),
    }
