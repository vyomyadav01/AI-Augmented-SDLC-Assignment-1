# Constitution - Part 1B: Natural Language Reminder Agent

## 1. Scope & Determinism
- Process natural language reminders into structured outputs across deterministic and non-deterministic layers.
- Strict schema adherence via Pydantic model contracts.

## 2. Guardrails & Safety
- Absolute ambiguity guardrails: Unresolvable relative temporal inputs must prompt for clarification.
- Default temporal calculations fallback strictly to UTC when no timezone offset is specified.

## 3. Evaluation Non-Negotiables
- Multi-layer evaluation harness must maintain an aggregate test pass rate >= 90%.
- Layer 1 (Schema) and Layer 2 (Invariant) checks require 100% compliance.
