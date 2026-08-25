import json
import os
from tools import get_context

SYSTEM_PROMPT = """
You are a read-only Student Success Advisor Support Agent.

Use only the supplied student context.
Do not invent facts.
Do not change or recalculate the stored risk prediction.
Explain SHAP as model explanation, not causality.
Explain reassessment as synthetic scenario-based estimation, not observed impact.
Do not make the final academic decision.
Do not write to the database.
There is no policy tool.
Keep answers short and clear for an academic advisor.
"""

def local_answer(student_key, question):
    ctx = get_context(student_key)
    p = ctx["prediction"]
    shap = ctx["shap"]
    interventions = ctx["interventions"]
    reassessment = ctx["reassessment"]
    q = question.lower()

    if "why" in q or "risk" in q:
        top = shap[:3]
        factors = ", ".join(
            f'{x["feature_name"]} ({x["feature_value"]})'
            for x in top
        )
        return (
            f'**{student_key}** has a stored risk probability of '
            f'**{p["risk_probability"]:.1%}**. '
            f'The main SHAP factors are {factors}. '
            'These explain the model prediction and are not causal claims.'
        )

    if "support" in q or "intervention" in q:
        if not interventions:
            return "No intervention is stored for this student."
        text = "; ".join(
            f'{x["intervention_type"]}: {x["proposed_action"]}'
            for x in interventions
        )
        return f'Proposed support: {text}. The advisor makes the final decision.'

    if "reassessment" in q or "scenario" in q:
        if not reassessment:
            return "No reassessment is stored for this student."
        text = "; ".join(
            f'{x["scenario"]}: {x["mean_reassessed_risk"]:.1%}'
            for x in reassessment
        )
        return (
            f'Reassessed risk by scenario: {text}. '
            'These are synthetic scenario estimates, not observed outcomes.'
        )

    return (
        f'**{student_key}** is '
        f'{"at risk" if p["predicted_label"] else "not at risk"} '
        f'with stored risk probability **{p["risk_probability"]:.1%}**. '
        'The advisor can review the SHAP factors, proposed support, and stored reassessment.'
    )

def ask_advisor_agent(student_key, question):
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
    api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip()
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21").strip()

    if not (endpoint and api_key and deployment):
        return local_answer(student_key, question)

    try:
        from openai import AzureOpenAI

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )

        ctx = get_context(student_key)

        response = client.chat.completions.create(
            model=deployment,
            temperature=0.1,
            max_tokens=500,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"STUDENT CONTEXT:\n{json.dumps(ctx, default=str)}\n\n"
                        f"QUESTION:\n{question}"
                    ),
                },
            ],
        )
        return response.choices[0].message.content

    except Exception:
        return local_answer(student_key, question)
