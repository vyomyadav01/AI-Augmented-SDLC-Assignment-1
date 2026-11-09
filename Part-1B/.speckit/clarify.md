# Clarifications: Part 1B Natural-Language Reminder Assistant

## Edge Cases & Ambiguities Resolved
1. **Relative Datetime Parsing**: All relative temporal expressions (e.g., "in 2 hours", "tomorrow at 5 PM") resolve deterministically against a reference execution timestamp injected during invocation.
2. **Missing Mandatory Information**: If an input specifies an action without a time/date, or a time without a recognizable task, the system must set `needs_clarification = True` and emit an explicit prompt request.
3. **Temporal Validity**: If an interpreted time occurs in the past relative to the injected current time, it must advance to the next logical occurrence or trigger clarification if ambiguous.
4. **Timezone Representation**: All resolved target timestamps must adhere strictly to ISO-8601 UTC formatting.
