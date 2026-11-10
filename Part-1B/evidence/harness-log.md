# Harness Execution Log - Part 1B

## Execution Metadata
- Model: `gemini-flash-lite-latest`
- Temperature: `0.0`
- Response Mode: Structured JSON (`application/json`)
- Evaluation Gate: Layer 1 (Schema) 100%, Layer 2 (Invariants) 100%, Layer 3 (Semantic) >= 90%
- Authentication: Secure header via `x-goog-api-key`

## Baseline Evaluation (Pre-Repair)
- Source: `Part-1B/evidence/baseline-results.json`
- Total Cases: 15
- Layer 1 (Schema): 100.0% (15/15)
- Layer 2 (Invariants): 100.0% (15/15)
- Layer 3 (Semantic Accuracy): 53.3% (8/15)

### Baseline Failure Diagnosis
- Adversarial & Ambiguous Inputs: Inputs containing ambiguous strings or empty whitespace failed semantic clarification expectations due to loose initial system instructions.
- Date/Time & Recurrence Normalization: Temporal terms ("tomorrow", "9:30 AM", "daily") were captured as free-form strings rather than normalized ISO-8601 dates and constrained recurrence enums.
- Root Cause: Initial un-tuned prompt lacked explicit schema boundary rules, ISO constraints, and recurrence enumerations (`daily`, `weekly`, `monthly`, `none`).

## Repair Strategy
1. Authored structured system instructions in `Part-1B/prompts/system_prompt.txt` enforcing strict output contracts.
2. Hardened `ReminderOutput` schema with Pydantic field validators ensuring ISO date compliance and enumerated recurrence rules.
3. Routed all inputs (including empty/whitespace strings) through live zero-shot inference with exponential backoff on transient errors.

## Final Evaluation (Post-Repair)
- Source: `Part-1B/evidence/eval-results.json`
- Total Cases: 15
- Layer 1 (Schema Validation): 100.0% (15/15) PASSED
- Layer 2 (Business Invariants): 100.0% (15/15) PASSED
- Layer 3 (Semantic Ground Truth): 100.0% (15/15) PASSED

## Residual Risks & Limitations
- Network Dependency: Live model inference relies on API uptime; transient HTTP 503/429 errors are mitigated via exponential backoff (up to 3 retries).
- Context Horizon: Ambiguous relative dates (e.g., "next Friday") require an anchored reference timestamp for deterministic temporal resolution.
