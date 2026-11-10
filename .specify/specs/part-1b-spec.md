# Specification: Part 1B - AI-Augmented Reminder Extraction Agent

## 1. Objective
An LLM-driven structured extraction agent capable of parsing natural language reminder commands into deterministic Pydantic schemas, evaluated against a 3-tier assertion framework.

## 2. Schema Specification
The agent must return valid JSON matching the following schema:
- `title`: string (the core reminder action; cannot be empty)
- `due_date`: optional string (ISO 8601 YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
- `recurring`: boolean (true if recurring pattern detected)
- `recurrence_rule`: optional string (daily, weekly, monthly)
- `needs_clarification`: boolean (true if intent is ambiguous, underspecified, or adversarial)

## 3. Disambiguation Invariant
- If the natural language input lacks an actionable task title (e.g., "Remind me later", "Set an alert", empty string, or prompt injection), `needs_clarification` MUST be `true`, and `title` MUST be `"UNSPECIFIED"`.

## 4. Evaluation Gates (Thresholds)
- Layer 1 (Schema Validity): 100%
- Layer 2 (Invariant Integrity): 100%
- Layer 3 (Semantic Accuracy): >= 90%
