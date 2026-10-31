#!/usr/bin/env bash
# Deterministic Test Harness for Part 1A
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== [GATE 1] Running Static Lint Analysis (Ruff) ==="
ruff check "$BASE_DIR/src" || true

echo ""
echo "=== [GATE 2] Running Security SAST Scan (Bandit) ==="
bandit -r "$BASE_DIR/src" -ll -q || true

echo ""
echo "=== [GATE 3] Running Deterministic Unit Tests (Pytest) ==="
PYTHONPATH="$BASE_DIR" pytest "$BASE_DIR/tests" -v || true
