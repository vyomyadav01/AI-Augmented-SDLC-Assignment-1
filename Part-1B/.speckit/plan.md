# Technical Architecture Plan: Part 1B

## 1. System Architecture
- **Agent Orchestrator (`src/agent.py`)**: Structured prompting engine interfacing with LLM completion, passing fixed instructions, reference timestamp, and input reminder string.
- **Data & Contract Layer**: Pydantic schema enforcing required output structures (`title`, `trigger_time`, `recurrence`, `needs_clarification`, `clarification_prompt`).
- **3-Tier Non-Deterministic Harness (`.harness/run_eval.py`)**:
  - **Layer 1 (Schema Guard)**: JSON parsing and Pydantic contract validation.
  - **Layer 2 (Invariant Guard)**: Deterministic business constraints (time boundaries, mutually exclusive clarification states).
  - **Layer 3 (Semantic Guard)**: Entity intent matching and ground-truth action fidelity.

## 2. Evaluation Strategy & Pass Threshold
- **Evaluation Dataset**: 15 distinct benchmark test cases in `evals/dataset.json`.
- **Pre-Declared Acceptance Thresholds**:
  - Layer 1 Schema Validity: 100% (15/15)
  - Layer 2 Invariant Compliance: 100% (15/15)
  - Layer 3 Semantic Quality: >= 90% (>= 14/15)
