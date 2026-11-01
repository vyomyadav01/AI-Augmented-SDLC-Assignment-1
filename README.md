# AI-Augmented SDLC Assignment 1
**Student Name:** Vyom Yadav
**Student ID:** 2026ns93132

## How to Run Harnesses

### 1. Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install ruff bandit pytest pydantic
```

### 2. Part 1A Deterministic Harness
```bash
ruff check Part-1A/
bandit -r Part-1A/src/
pytest Part-1A/tests/
```

### 3. Part 1B Non-Deterministic Evaluation Pipeline
```bash
python3 Part-1B/.harness/run_eval.py
```
