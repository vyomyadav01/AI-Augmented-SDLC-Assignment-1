import json
from pathlib import Path
from src.models import Task, Priority

class TaskStorage:
    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = Path(filepath)

    def load_all(self) -> list:
        if not self.filepath.exists():
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task.from_dict(d) for d in data]

    def save_all(self, tasks: list):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2)

    def list_tasks(self, tag: str = None, status: str = None, sort_by: str = "id") -> list:
        tasks = self.load_all()
        if tag:
            tasks = [t for t in tasks if tag in t.tags]
        if status:
            tasks = [t for t in tasks if t.status == status]
        if sort_by == "priority":
            priority_map = {Priority.LOW: 1, Priority.MED: 2, Priority.HIGH: 3}
            tasks.sort(key=lambda t: priority_map[t.priority])
        else:
            tasks.sort(key=lambda t: t.id)
        return tasks
