# Constitution - Part 1A: Smart Todo CLI

## 1. Scope & Determinism
- All functional behaviors must be strictly deterministic (identical inputs must produce identical outputs and exit codes).
- Data persistence must utilize a local JSON flat-file without external database dependencies.

## 2. Engineering Constraints
- Standard Python 3.10+ modular architecture.
- Comprehensive input validation on all user arguments.
- Standard POSIX exit codes: 0 for success, non-zero (1) for error/validation failure.

## 3. Harness Non-Negotiables
- Static analysis (Ruff) must pass with zero lint errors.
- Security scan (Bandit) must yield zero Medium or High severity vulnerabilities.
- Unit and contract test suite (Pytest) must achieve a 100% pass rate.
