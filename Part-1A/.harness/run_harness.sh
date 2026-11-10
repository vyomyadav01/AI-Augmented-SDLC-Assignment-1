#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RESULTS_DIR="$BASE_DIR/evidence/harness-results"
mkdir -p "$RESULTS_DIR"

FAILED=0

echo "=== [GATE 1] Running Static Lint Analysis (Ruff) ==="
if ruff check "$BASE_DIR/src" > "$RESULTS_DIR/ruff.txt" 2>&1; then
    cat "$RESULTS_DIR/ruff.txt"
    echo "[GATE 1 PASS] Ruff lint clean."
else
    cat "$RESULTS_DIR/ruff.txt"
    echo "[GATE 1 FAIL] Ruff detected violations."
    FAILED=1
fi

echo ""
echo "=== [GATE 2] Running Security SAST Scan (Bandit) ==="
if bandit -r "$BASE_DIR/src" -ll -q > "$RESULTS_DIR/bandit.txt" 2>&1; then
    cat "$RESULTS_DIR/bandit.txt"
    echo "[GATE 2 PASS] Bandit security scan clean."
else
    cat "$RESULTS_DIR/bandit.txt"
    echo "[GATE 2 FAIL] Bandit detected security issues."
    FAILED=1
fi

echo ""
echo "=== [GATE 3] Running Deterministic Unit Tests (Pytest) ==="
if PYTHONPATH="$BASE_DIR" pytest "$BASE_DIR/tests" -v > "$RESULTS_DIR/pytest.txt" 2>&1; then
    cat "$RESULTS_DIR/pytest.txt"
    echo "[GATE 3 PASS] Pytest suite passed."
else
    cat "$RESULTS_DIR/pytest.txt"
    echo "[GATE 3 FAIL] Pytest failures detected."
    FAILED=1
fi

echo ""
if [ $FAILED -ne 0 ]; then
    echo "=== HARNESS VERDICT: FAILED ==="
    exit 1
else
    echo "=== HARNESS VERDICT: ALL GATES PASSED ==="
    exit 0
fi
