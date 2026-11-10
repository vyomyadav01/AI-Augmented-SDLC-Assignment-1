# Specification: Part 1A - Deterministic CLI Task Manager

## 1. Objective
A deterministic command-line task manager written in Python supporting complete CRUD operations with strict JSON schema serialization, deterministic exit codes, and automated CI test gates.

## 2. Requirements & Acceptance Criteria
- **AC1 (Creation Status)**: Adding a task via CLI saves it to JSON storage with initial status `pending` and assigns an auto-incrementing integer ID.
- **AC2 (Query Filtering)**: Filtering by tag and status returns matching subsets deterministically.
- **AC3 (Priority Sorting)**: Listing with `--sort priority` orders tasks by high > med > low.
- **AC4 (Exit Codes & Errors)**: Non-existent IDs or invalid parameter updates output to `stderr` and exit with code `1`. Successful operations exit with `0`.
- **Validation**: Empty title or whitespace-only title throws a validation exception and exits with `1`.

## 3. Tooling & Verification Gates
- Static Lint: Ruff (`ruff check`)
- SAST Security: Bandit (`bandit -r src/`)
- Unit Testing: Pytest with 100% AC assertion coverage.
