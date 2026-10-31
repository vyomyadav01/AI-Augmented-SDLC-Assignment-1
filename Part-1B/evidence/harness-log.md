# Part 1B Non-Deterministic Evaluation & Harness Log

## 1. Model & Configuration
- **Application Scope**: Natural-Language Reminder Agent (parsing unstructured temporal intent into structured JSON).
- **Schema Engine**: Pydantic v2 `ReminderOutput` model.
- **Evaluation Dataset**: `Part-1B/evals/dataset.json` (15 diverse evaluation cases covering explicit dates, relative times, recurrences, underspecified inputs, empty strings, and prompt injection attempts)[cite: 7].

## 2. Evaluation Threshold & Scoring Strategy
- **Pre-declared Threshold**: 80.0% aggregate pass rate across all layers.
- **Harness Layers**:
  1. **Layer 1 (Structural)**: Pydantic schema contract conformance.
  2. **Layer 2 (Invariants/Properties)**: Invariant validation (`needs_clarification=True` must include a non-null `clarification_question`; non-clarified cases must have a title)[cite: 6, 8].
  3. **Layer 3 (Semantic/Quality)**: Fuzzy semantic matching for title, recurrence enum correctness, and appropriate clarification flagging[cite: 6, 8].

## 3. Evaluation Results
- **Total Test Cases**: 15[cite: 7, 8]
- **Cases Passed**: 15
- **Cases Failed**: 0[cite: 8]
- **Aggregate Score**: 100.0% (Threshold: 80.0%)[cite: 8]
- **Status**: **PASS**[cite: 8]
- **Detailed Log**: Preserved in `Part-1B/evidence/eval-results.json`[cite: 8].

## 4. Failure and Repair Evidence (Development Iteration)
- **Initial Iteration Issue**: Underspecified queries lacking time/date parameters (e.g., Case 8 "Pay electricity bill" and Case 15 "Call John") were initially marked with `needs_clarification=False` and assigned a null scheduled timestamp.
- **Feedback Provided**: Invariant violation in Layer 2 (a task cannot be scheduled without a valid date/time or recurrence pattern; it must trigger a clarification prompt)[cite: 6, 8].
- **Repair**: Updated parsing rules in `src/agent.py` so that missing temporal bounds trigger `needs_clarification=True` with an explicit clarification question[cite: 6, 8].
- **Re-evaluation Result**: All 15 cases conformed to structural and invariant constraints, achieving a 100% pass score[cite: 8].

## 5. Human Acceptance Decision
- **Final Decision**: **ACCEPT**
- **Residual Risks & Limitations**: Complex nested temporal expressions (e.g., "every alternate Tuesday excluding holidays") and timezone handling across geographical borders require a full LLM-based semantic parser and dedicated calendar API integration before production release[cite: 8].
