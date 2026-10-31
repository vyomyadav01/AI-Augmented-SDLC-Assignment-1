# Feature Specification: Reminder Parsing Agent

## Requirements
- Parse freeform user input into structured reminder entities (title, due_date, tags, priority).
- Handle ambiguous datetime inputs by flagging `needs_clarification: true`.
- Output strictly validated JSON matching the target schema.

## Acceptance Criteria
- **AC1**: High-confidence absolute and relative dates must parse accurately to ISO-8601 strings.
- **AC2**: Missing temporal components must prompt for follow-up without hallucinating arbitrary timestamps.
- **AC3**: 3-layer evaluation harness benchmark must achieve a pass rate >= 90%.
