import json
from pathlib import Path
from typing import List
from .models import Task, Priority, Status

class TaskStorage:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)

    def load_tasks(self) -> List[Task]:
        if not self.file_path.exists():
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [
                Task(
                    id=item["id"],
                    title=item["title"],
                    tags=item.get("tags", []),
                    priority=Priority(item.get("priority", "low")),
                    status=Status(item.get("status", "pending"))
                )
                for item in data
            ]

    def save_tasks(self, tasks: List[Task]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([task.__dict__ for task in tasks], f, indent=2)

    def get_sorted_tasks(self, sort_by: str = "id") -> List[Task]:
        tasks = self.load_tasks()
        if sort_by == "priority":
            # Buggy initial logic: LOW first instead of HIGH first
            priority_order = {Priority.LOW: 1, Priority.MED: 2, Priority.HIGH: 3}
            return sorted(tasks, key=lambda t: priority_order.get(t.priority, 4))
        return sorted(tasks, key=lambda t: t.id)
