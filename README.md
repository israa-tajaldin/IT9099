# Beyond Prediction: An Explainable AI Framework for Early Risk Detection, Personalised Intervention Planning, and Dynamic Reassessment of At-Risk Students

MSc in Artificial Intelligence — Bahrain Polytechnic
Author: Israa Tajaldin (ID: 12010745)
Supervisor: Dr. Shahnawaz Khan

---

## 1. Overview

This repository contains the full implementation of a closed-loop, explainable AI framework for identifying at-risk students, generating personalised intervention plans, and dynamically reassessing risk after simulated support. The system integrates five stages: supervised risk classification, SHAP-based explainability, rule-based intervention planning, an agentic natural-language reporting layer, and a synthetic-data reassessment module.

The repository is organised into two logical zones:

- **`notebooks/`** — exploratory work (EDA, preprocessing trials, model comparison). These notebooks document the analytical decisions but are not part of the production pipeline.
- **`src/`** — the stable, callable pipeline that reproduces the final results and is used by all downstream modules (explainability, intervention, reassessment, agentic reporting).

## 2. Repository Structure

```
thesis-repo/
├── notebooks/              # exploratory analysis, not production code
├── data/
│   ├── raw/                 # anonymised source exports (not included — see Section 5)
│   ├── interim/              # cleaned, pre-aggregation
│   └── processed/            # final student-semester feature table
├── src/
│   ├── data/                 # loading and preprocessing
│   ├── features/              # feature schema construction
│   ├── models/                # training, evaluation, model selection
│   ├── explainability/         # SHAP module
│   ├── intervention/           # rule-based intervention engine
│   ├── reassessment/            # synthetic progression and delta-risk evaluation
│   └── agent/                   # LangChain + Azure OpenAI advisor report generator
├── models/                  # saved model artefacts
├── reports/                 # figures and evaluation outputs
├── tests/                   # unit tests
├── requirements.txt
└── README.md
```

## 3. Environment Setup

The project was developed using **Python 3.11**.

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd thesis-repo
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Core libraries used: `pandas`, `numpy`, `scikit-learn`, `xgboost`, `shap`, `matplotlib`, `langchain`, `openai` (Azure OpenAI SDK), `scipy` (for Wilcoxon signed-rank testing).

## 4. Configuration

Copy the environment template and fill in the required credentials before running the agentic reporting layer:

```bash
cp .env.example .env
```

Required variables:

```
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

The `.env` file is excluded from version control via `.gitignore`. No credentials are stored in the repository.

## 5. Data Availability

This project uses anonymised secondary institutional data from Bahrain Polytechnic's Banner (Student Information System) and Moodle (LMS), governed by Bahrain's Personal Data Protection Law (Law No. 30 of 2018).

**Raw data is not included in this repository.** In accordance with the data governance conditions under which access was granted, the source data cannot be redistributed. Researchers wishing to reproduce results on the same population would need to request access through Bahrain Polytechnic's Deanship of Applied Research and Entrepreneurship.

To support reproducibility of the *pipeline logic* without institutional access, a synthetic sample dataset with the same schema is provided at `data/sample/synthetic_sample.csv`. This allows the full pipeline to be executed end-to-end for verification purposes, though results will not match those reported in the thesis.

## 6. Reproducing the Pipeline

The following sequence reproduces the results reported in the thesis, assuming access to the raw anonymised dataset placed under `data/raw/`.

### Step 1 — Preprocessing and Feature Construction
```bash
python -m src.data.preprocess
python -m src.features.build_features
```
Produces the student-semester aggregated feature table at `data/processed/features.csv`, including the mutable/immutable feature split used later by the reassessment module.

### Step 2 — Model Training and Selection
```bash
python -m src.models.train
python -m src.models.evaluate
```
Trains Logistic Regression, Random Forest, and XGBoost using group-aware cross-validation (to prevent student-level data leakage), and outputs a comparison table (F1, AUC-ROC, precision, recall, fairness metrics across protected groups). The best-performing model is saved to `models/best_model.pkl`.

### Step 3 — Explainability
```bash
python -m src.explainability.shap_module
```
Generates global and per-student SHAP attributions using the saved best model, saved to `models/shap_values.pkl` and `reports/figures/`.

### Step 4 — Intervention Planning
```bash
python -m src.intervention.intervention_engine
```
Maps SHAP-derived risk factors to a structured intervention taxonomy for each at-risk student.

### Step 5 — Synthetic Reassessment
```bash
python -m src.reassessment.synthetic_progression
python -m src.reassessment.delta_risk_eval
```
Applies intervention-specific perturbation distributions (calibrated to published effect sizes) to mutable features only, re-scores the updated profiles through the saved model, and evaluates risk change using the Wilcoxon signed-rank test.

### Step 6 — Advisor Report Generation
```bash
python -m src.agent.advisor_report_generator
```
Combines the outputs of Steps 2–5 into a personalised natural-language advisor/student report using LangChain and Azure OpenAI GPT-4o-mini. Requires the `.env` configuration described in Section 4.

## 7. Reproducibility Notes

- **Random seeds** are fixed (`random_state=42`) across all model training, train/test splitting, and synthetic sampling steps to ensure deterministic results across runs.
- **Cross-validation** uses `GroupKFold` at the student ID level to avoid data leakage between splits.
- **Synthetic reassessment results** are scenario-based estimates, not evidence of real intervention outcomes, and should be interpreted accordingly (see Section 9 of the thesis).
- Protected attributes (fairness audit variables) are excluded from model training features and used only in the fairness evaluation step in `src/models/evaluate.py`.

## 8. AI Usage Statement

Generative AI tools were used during this project for code scaffolding, proofreading, and drafting support, in accordance with Section 7.5 of the MSc AI Thesis Handbook. All AI-assisted code and text were critically reviewed, tested, and adapted by the author. The literature review, methodology, and critical analysis sections were authored independently, with AI tools used only for language refinement.

## 9. License and Data Governance

This repository is provided for academic assessment purposes as part of the MSc in Artificial Intelligence at Bahrain Polytechnic. Redistribution of the raw institutional dataset is not permitted under the terms of data access. Contact the author or Dr. Shahnawaz Khan (Deanship of Applied Research and Entrepreneurship) for data access inquiries.
