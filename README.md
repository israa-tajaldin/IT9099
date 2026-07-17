# Beyond Prediction: An Explainable AI Framework for Early Risk Detection, Personalised Intervention Planning, and Dynamic Reassessment of At-Risk Students

MSc in Artificial Intelligence - Bahrain Polytechnic  

Author: Israa Tajaldin (ID: 12010745)  

Supervisor: Dr. Shahnawaz Khan  

---

## 1. Overview

This project develops a closed loop AI framework for the early identification of students who are academically at risk. The framework combines prediction, SHAP explanations, personalised intervention planning, synthetic student progression, and dynamic reassessment.

## 2. Repository Structure

```
Main/
├── notebooks/              # exploratory analysis, not production code
├── data/
│   ├── raw/                 # anonymised source exports (not included — see Section 4)
│   └── processed/            # final student-semester feature table
├── src/
├── results/                 # figures and evaluation outputs
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


## 4. Data Availability

This project uses anonymised secondary institutional data from Bahrain Polytechnic's Banner (Student Information System) and Moodle (LMS), governed by Bahrain's Personal Data Protection Law (Law No. 30 of 2018).

**Raw data is not included in this repository.** In accordance with the data governance conditions under which access was granted, the source data cannot be redistributed. Researchers wishing to reproduce results on the same population would need to request access through Bahrain Polytechnic's Deanship of Applied Research and Entrepreneurship.

To support reproducibility of the *pipeline logic* without institutional access, a synthetic sample dataset with the same schema will be provided at `data/sample/synthetic_sample.csv`. This allows the full pipeline to be executed end-to-end for verification purposes, though results will not match those reported in the thesis.


