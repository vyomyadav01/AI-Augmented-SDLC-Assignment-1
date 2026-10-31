# Constitution - Part 1A: Smart Todo CLI

## 1. Scope & Determinism
- Sabhi functional behaviors strictly deterministic honge (same input delivers identical output and exit code).
- Persistence local JSON file me hogi without external databases.

## 2. Engineering Constraints
- Python 3.10+ standard libraries and clean modular structure.
- Input validation on all user arguments.
- Standard exit codes: 0 for success, non-zero (1) for error/validation failure.

## 3. Harness Non-Negotiables
- Static analysis (Ruff) pass hona mandatory hai.
- Security scan (Bandit) me koi medium ya high severity finding nahi honi chahiye.
- Unit aur contract tests 100% pass hone chahiye.
