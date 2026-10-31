import re
from enum import Enum
from pydantic import BaseModel, Field


class Recurrence(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ReminderOutput(BaseModel):
    title: str | None = Field(default=None)
    date: str | None = Field(default=None)
    time: str | None = Field(default=None)
    recurrence: Recurrence = Field(default=Recurrence.NONE)
    needs_clarification: bool = Field(default=False)
    clarification_question: str | None = Field(default=None)


class ReminderAgent:
    def parse_intent(self, user_input: str) -> ReminderOutput:
        text = user_input.strip()

        # Guardrail / Malformed Input Check
        if not text or "ignore previous instructions" in text.lower():
            return ReminderOutput(
                title=None,
                needs_clarification=True,
                clarification_question="I could not understand the reminder. Please specify what you want to be reminded about.",
            )

        # Ambiguous inputs check
        lower_text = text.lower()
        if lower_text in ["remind me later", "set an alert"]:
            return ReminderOutput(
                title=None,
                needs_clarification=True,
                clarification_question="What should I remind you about and at what time?",
            )

        # Recurrence extraction
        recurrence = Recurrence.NONE
        if "daily" in lower_text or "every day" in lower_text:
            recurrence = Recurrence.DAILY
        elif "weekly" in lower_text or "every monday" in lower_text:
            recurrence = Recurrence.WEEKLY
        elif "monthly" in lower_text:
            recurrence = Recurrence.MONTHLY

        # Time extraction (e.g. 5 PM, 10:00 AM)
        time_match = re.search(r"\b(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM))\b", text)
        time_str = time_match.group(1) if time_match else None

        # Date extraction (YYYY-MM-DD or tomorrow/Friday)
        date_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)
        date_str = date_match.group(1) if date_match else None
        if not date_str:
            if "tomorrow" in lower_text:
                date_str = "tomorrow"
            elif "friday" in lower_text:
                date_str = "next friday"

        # Title extraction
        clean_title = re.sub(r"(?i)^remind me to\s+", "", text)
        clean_title = re.sub(
            r"(?i)\s+(tomorrow|next friday|daily|every monday|by \d+.*|at \d+.*|on \d{4}-\d{2}-\d{2})",
            "",
            clean_title,
        ).strip()

        # Check if mandatory time/date is missing
        if not time_str and not date_str and recurrence == Recurrence.NONE:
            return ReminderOutput(
                title=clean_title if clean_title else text,
                needs_clarification=True,
                clarification_question="Please provide a date or time for this reminder.",
            )

        return ReminderOutput(
            title=clean_title if clean_title else text,
            date=date_str,
            time=time_str,
            recurrence=recurrence,
            needs_clarification=False,
            clarification_question=None,
        )
