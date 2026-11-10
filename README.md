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

## AI Usage Statement
In accordance with course guidelines, AI coding assistants (Gemini / Claude) were utilized as structured generators under strict human supervision. AI proposals were constrained by pre-authored specifications (`.speckit/`) and subjected to automated deterministic (Ruff, Bandit, Pytest) and non-deterministic (3-tier evaluation harness) verification gates. All final architecture decisions, test case designs, and repair validations were authored and reviewed by the student.

## Environment Configuration
To run Part-1B evaluations against live Gemini models, configure your API key via `.env` or export it in your shell environment:
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```
The client authenticates securely via the `x-goog-api-key` HTTP header rather than URL query parameters.

## AI Usage Statement
LLM-assisted code generation was constrained by pre-authored specifications (`.speckit/`). Initial un-tuned model outputs exhibited edge-case failures across ambiguous clarify triggers and non-standard datetime formats, which were systematically remediated through layered schema validation and prompt refinement.
