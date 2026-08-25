# Simple Student Success Advisor Prototype

## What it contains

Only three interface pages:

1. Dashboard
2. Student Review
3. Advisor Assistant

The system uses:

- Python
- Streamlit
- SQLite
- One optional Azure GPT advisor-support agent

The GPT assistant is read-only. It explains stored evidence only.

The advisor is the only one who saves the final decision.

The app displays reassessment results already produced by the thesis pipeline.

## Run

```bash
pip install -r requirements.txt
python seed_demo.py
streamlit run app.py
```

The included data is synthetic demonstration data only , for publishing in the repository.

## Files

```text
app.py
db.py
tools.py
advisor_agent.py
seed_demo.py
requirements.txt
.env.example
data/
```
