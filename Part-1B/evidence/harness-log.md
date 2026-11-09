# Non-Deterministic Evaluation Harness Log (Part 1B)

## 1. Evaluation Configuration
- **Target Application**: Natural-Language Reminder Assistant (`src/agent.py`)
- **Evaluation Runner**: `.harness/run_eval.py`
- **Evaluation Dataset**: `evals/dataset.json` (15 test cases)
- **Declared Pass Threshold**:
  - Layer 1 (Schema Conformance): 100% (15/15)
  - Layer 2 (Invariant/Property Validation): 100% (15/15)
  - Layer 3 (Semantic/Quality Score): >= 90% (>= 14/15)

---

## 2. Initial Evaluation Run (Run #1 - FAILED)
- **Layer 1 (Schema)**: 15/15 PASS
- **Layer 2 (Invariants)**: 13/15 PASS (2 FAILURES)
- **Layer 3 (Semantic)**: 13/15 PASS
- **Aggregate Verdict**: **FAIL** (Did not satisfy 100% invariant gate)

### Failure Evidence Captured:
- **Test Case `TC-04`**: Input `"Remind me to submit the report"` (missing time anchor).
  - *Observed*: `needs_clarification == False`, `trigger_time == "2026-11-10T09:00:00Z"`
  - *Violation*: Invariant `INV-01` (Mandatory temporal specification missing; agent assumed next-day morning instead of prompting for clarification).
- **Test Case `TC-09`**: Input `"Call plumber at 2"` (ambiguous AM/PM specification).
  - *Observed*: `trigger_time == "2026-11-10T02:00:00Z"`
  - *Violation*: Invariant `INV-03` (Ambiguous time parsed as 2:00 AM without clarification).

---

## 3. Repair Cycle (Self-Healing via Failure Evidence)
- **Failure Evidence Provided to Agent**: Raw JSON evaluation trace, failed invariant IDs (`INV-01`, `INV-03`), and relevant input prompts.
- **Application Modifications**:
  - Modified `src/agent.py` system instructions under `[Disambiguation Rules]` to explicitly forbid default assumptions for unspecified hours or missing times. Added explicit instruction: *"When temporal boundaries are missing, vague, or lack AM/PM disambiguation, you MUST set `needs_clarification: true`."*
  - Added post-processing guardrail checking that whenever `needs_clarification` is true, `clarification_prompt` contains actionable follow-up guidance.

---

## 4. Re-Evaluation Run (Run #2 - Post-Repair - PASSED)
- **Aggregated Gate Scores**:
  - Layer 1 Schema Conformance: 15/15 (100%)
  - Layer 2 Invariant Compliance: 15/15 (100%)
  - Layer 3 Semantic Score: 15/15 (100% threshold met, mean fidelity: 0.98)
- **Aggregate Verdict**: **PASS**

---

## 5. Human Review & Acceptance
- **Reviewer Decision**: **ACCEPTED**
- **Justification**: Prompt instructions and guardrails correctly resolved default-time hallucinations while preserving semantic extraction fidelity across all nominal inputs.
- **Residual Risks & Production Controls**: Lacks native device timezone auto-detection (currently relies on UTC normalization) and requires rate-limiting on LLM endpoints to mitigate token denial-of-service in production.
