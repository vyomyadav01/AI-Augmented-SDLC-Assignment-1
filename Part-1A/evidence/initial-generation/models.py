import os
from enum import Enum
from dataclasses import dataclass

class Priority(str, Enum):
    LOW = "low"
    MED = "med"
    HIGH = "high"

class Status(str, Enum):
    PENDING = "pending"
    DONE = "done"

@dataclass
class Task:
    id: int
    title: str
    tags: list = None
    priority: Priority = Priority.LOW
    status: Status = Status.PENDING
