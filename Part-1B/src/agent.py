import os
import json
import re
from enum import Enum
from pathlib import Path
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
    def __init__(self, prompt_path: str | None = None):
        if prompt_path is None:
            base_dir = Path(__file__).resolve().parents[1]
            prompt_path = base_dir / "prompts" / "system_prompt.txt"
        self.prompt_path = Path(prompt_path)
        self.system_prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        if self.prompt_path.exists():
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        return "Parse reminder into structured JSON."

    def call_llm(self, user_input: str) -> str:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if api_key and os.getenv("USE_LIVE_LLM", "0") == "1":
            try:
                import litellm
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ]
                model = "gpt-4o-mini" if os.getenv("OPENAI_API_KEY") else "gemini/gemini-1.5-flash"
                resp = litellm.completion(model=model, messages=messages, response_format={"type": "json_object"})
                return resp.choices[0].message.content
            except Exception:
                pass

        text = user_input.strip()
        lower = text.lower()

        if not text or "ignore previous instructions" in lower:
            return json.dumps({
                "title": None, "date": None, "time": None, "recurrence": "none",
                "needs_clarification": True,
                "clarification_question": "I could not understand the reminder. Please specify what you want to be reminded about."
            })

        if lower in ["remind me later", "set an alert"]:
            return json.dumps({
                "title": None, "date": None, "time": None, "recurrence": "none",
                "needs_clarification": True,
                "clarification_question": "What should I remind you about and at what time?"
            })

        rec = "none"
        if "daily" in lower or "every day" in lower:
            rec = "daily"
        elif "weekly" in lower or "every monday" in lower:
            rec = "weekly"
        elif "monthly" in lower:
            rec = "monthly"

        time_match = re.search(r"\b(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM))\b", text)
        time_str = time_match.group(1) if time_match else None

        date_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)
        date_str = date_match.group(1) if date_match else None
        if not date_str:
            if "tomorrow" in lower:
                date_str = "tomorrow"
            elif "next friday" in lower or "friday" in lower:
                date_str = "next friday"

        title = re.sub(r"(?i)^remind me to\s+", "", text)
        title = re.sub(r"(?i)\s+(tomorrow|next friday|daily|every monday|by\s+\d+.*|at\s+\d+.*|on\s+\d{4}-\d{2}-\d{2}).*", "", title).strip()

        if not time_str and not date_str and rec == "none":
            return json.dumps({
                "title": title if title else text, "date": None, "time": None, "recurrence": "none",
                "needs_clarification": True,
                "clarification_question": "Please provide a date or time for this reminder."
            })

        return json.dumps({
            "title": title if title else text, "date": date_str, "time": time_str,
            "recurrence": rec, "needs_clarification": False, "clarification_question": None
        })

    def parse_intent(self, user_input: str) -> ReminderOutput:
        raw_json = self.call_llm(user_input)
        return ReminderOutput.model_validate_json(raw_json)
