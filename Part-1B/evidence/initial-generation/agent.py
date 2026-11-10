# Initial Agent Baseline (Pre-Repair)
import json
import re
from src.agent import ReminderOutput

class InitialReminderAgent:
    def parse_intent(self, user_input: str) -> ReminderOutput:
        return ReminderOutput(
            title=user_input.strip(),
            date=None,
            time=None,
            recurrence="none",
            needs_clarification=False,
            clarification_question=None
        )
