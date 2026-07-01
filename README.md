# Beyond Prediction: An Explainable AI Framework for Early Risk Detection, Personalised Intervention Planning, and Dynamic Reassessment of At-Risk Students

MSc in Artificial Intelligence - Bahrain Polytechnic  

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


