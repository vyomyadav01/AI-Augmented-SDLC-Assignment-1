import os
import re
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

RecurrenceType = Literal["daily", "weekly", "monthly", "none"]

class ReminderOutput(BaseModel):
    title: Optional[str] = Field(default=None, description="Actionable title of the reminder. None or empty if ambiguous.")
    due_date: Optional[str] = Field(default=None, description="ISO format due date (YYYY-MM-DD or ISO-8601 timestamp).")
    recurring: bool = Field(default=False, description="Whether this reminder repeats.")
    recurrence_rule: Optional[RecurrenceType] = Field(default=None, description="Allowed: daily, weekly, monthly, none.")
    needs_clarification: bool = Field(default=False, description="True if input lacks actionable action, clear time, or is ambiguous.")

    @field_validator("due_date")
    @classmethod
    def validate_iso_due_date(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        iso_pattern = r"^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)?$"
        if not re.match(iso_pattern, v.strip()):
            raise ValueError(f"due_date '{v}' must be a valid ISO format date/timestamp (YYYY-MM-DD or ISO-8601).")
        return v.strip()

    @field_validator("recurrence_rule")
    @classmethod
    def validate_recurrence_rule(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        val = v.strip().lower()
        allowed = {"daily", "weekly", "monthly", "none"}
        if val not in allowed:
            raise ValueError(f"recurrence_rule '{v}' must be one of {allowed}.")
        return val


def load_system_prompt() -> str:
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "system_prompt.txt"
    if prompt_path.exists():
        return prompt_path.read_text().strip()
    return "Extract reminder into JSON with title, due_date, recurring, recurrence_rule, needs_clarification."


def call_llm(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

    model = "gemini-flash-lite-latest"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    system_instruction = load_system_prompt()

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"User Input:\n{prompt}"}
                ]
            }
        ],
        "systemInstruction": {
            "parts": [
                {"text": system_instruction}
            ]
        },
        "generationConfig": {
            "temperature": 0.0,
            "responseMimeType": "application/json"
        }
    }

    max_retries = 3
    last_error = None

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            last_error = f"HTTP {e.code}: {body}"
            if e.code in (503, 429):
                time.sleep(2.0 * (attempt + 1))
                continue
            raise RuntimeError(f"Gemini API HTTP Error {e.code}: {body}")
        except Exception as e:
            last_error = str(e)
            time.sleep(1.5)

    raise RuntimeError(f"Exhausted live LLM retries: {last_error}")


def parse_reminder(text: str) -> ReminderOutput:
    raw_json = call_llm(text)
    data = json.loads(raw_json)
    return ReminderOutput.model_validate(data)
