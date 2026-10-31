# Assignment 1 - Spec-Driven Development & Harness Engineering

This repository contains two projects demonstrating Specification-Driven Development (SDD) and automated test harnesses:
- **Part-1A**: Deterministic Smart Todo CLI with Lint, Security (SAST), and Unit test gates.
- **Part-1B**: Non-Deterministic Natural-Language Reminder Agent with a 3-layer evaluation pipeline (Schema, Invariants, Semantic Quality).

## Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install ruff bandit pytest pydantic
