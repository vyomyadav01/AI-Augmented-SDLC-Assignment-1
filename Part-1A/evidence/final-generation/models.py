from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MED = "med"
    HIGH = "high"


class Task:
    def __init__(
        self,
        id: int,
        title: str,
        tags: list[str] | None = None,
        priority: Priority = Priority.LOW,
        status: str = "pending",
    ) -> None:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        self.id = id
        self.title = title.strip()
        self.tags = tags or []
        self.priority = (
            priority if isinstance(priority, Priority) else Priority(priority)
        )
        self.status = status

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "tags": self.tags,
            "priority": self.priority.value,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            tags=data.get("tags", []),
            priority=Priority(data.get("priority", "low")),
            status=data.get("status", "pending"),
        )
