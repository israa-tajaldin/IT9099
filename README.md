# Beyond Prediction: An Explainable AI Framework for Early Risk Detection, Personalised Intervention Planning, and Dynamic Reassessment of At-Risk Students

MSc in Artificial Intelligence - Bahrain Polytechnic  

Author: Israa Tajaldin (ID: 12010745)  

Supervisor: Dr. Shahnawaz Khan  

---

## 1. Overview

This project develops a closed loop AI framework for the early identification of students who are academically at risk. The framework combines: 
- Early academic risk prediction
- SHAP based explanations
- Personalised intervention decision support
- Dynamic risk reassessment
- An advisor support agent prototype


## 2. Repository Structure

The repository is organised into two main components.

**Experimental Notebooks**

The experimental_notebooks directory contains the research pipeline used to develop and evaluate the framework, including data preparation, machine learning model comparison, SHAP explanations, intervention support, synthetic progression, reassessment, fairness evaluation, and ablation studies.

The notebooks represent research experiments rather than production software.

```
experimental_notebooks/
├── notebooks/                      # Research and experimental notebooks
├── data/
│   ├── raw/                        # Private source data, not included
│   └── processed/                  # Processed research data, not included
├── results/
│   ├── baseline_models/            # Baseline model outputs
│   ├── model_comparison/           # Cross-validation and model comparison results
│   ├── final_model/                # Final model evaluation outputs
│   ├── explainability/             # SHAP explanation outputs
│   ├── interventions/              # Intervention decision-support results
│   ├── reassessment/               # Synthetic progression and reassessment results
│   ├── ablation/                   # Ablation study results
│   ├── figures/                    # Figures used in the thesis
│   └── data_dictionary.xlsx        # Dataset field definitions
└── requirements.txt
```


**Advisor Support Agent Prototype**

The advisor_support_agent_prototype directory contains a proof of concept interface demonstrating how the framework outputs could be presented to an academic advisor.

The prototype retrieves structured model outputs and generates advisor friendly summaries while keeping final intervention decisions with the human advisor.
```
 advisor_support_agent_prototype/
    ├── app.py                      # Streamlit advisor interface
    ├── db.py                       # SQLite database functions
    ├── tools.py                    # Controlled advisor tools
    ├── advisor_agent.py            # Advisor support agent
    ├── seed_demo.py                # Creates demo data
    ├── requirements.txt
    └── data/
        └── prototype.db            # Local prototype database
```
#### Prototype Disclaimer
The advisor support agent is a proof-of-concept and cannot run directly from this repository because it depends on an internal database that is not publicly available due to data privacy restrictions.

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


## 4. Data Availability

This project uses anonymised secondary institutional data from Bahrain Polytechnic's Banner (Student Information System) and Moodle (LMS), governed by Bahrain's Personal Data Protection Law (Law No. 30 of 2018) and are not included in this repository.

Only code, documentation, safe aggregate results, and demonstration resources suitable for public sharing are included.


**Raw data is not included in this repository.** In accordance with the data governance conditions under which access was granted, the source data cannot be redistributed. Researchers wishing to reproduce results on the same population would need to request access through Bahrain Polytechnic's Deanship of Applied Research and Entrepreneurship.



