import argparse
import sys

from src.models import Priority, Task
from src.storage import TaskStorage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smart Todo CLI")
    parser.add_argument("--db", default="tasks.json", help="Path to database file")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title", type=str)
    add_parser.add_argument("--tags", type=str, default="")
    add_parser.add_argument("--priority", choices=["low", "med", "high"], default="low")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", choices=["pending", "done"], default=None)
    list_parser.add_argument("--tag", type=str, default=None)
    list_parser.add_argument("--sort", choices=["priority", "id"], default="id")

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("target_id", type=int)
    update_parser.add_argument("--status", choices=["pending", "done"], default=None)
    update_parser.add_argument("--priority", choices=["low", "med", "high"], default=None)

    del_parser = subparsers.add_parser("delete")
    del_parser.add_argument("target_id", type=int)

    return parser


def main(args: list[str] | None = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return 1

    storage = TaskStorage(parsed.db)

    try:
        if parsed.command == "add":
            tasks = storage.load_all()
            next_id = max([t.id for t in tasks], default=0) + 1
            tags = [t.strip() for t in parsed.tags.split(",") if t.strip()] if parsed.tags else []
            new_task = Task(
                id=next_id,
                title=parsed.title,
                tags=tags,
                priority=Priority(parsed.priority),
                status="pending",
            )
            tasks.append(new_task)
            storage.save_all(tasks)
            print(f"Task {new_task.id} added: {new_task.title}")
            return 0

        elif parsed.command == "list":
            tasks = storage.list_tasks(tag=parsed.tag, status=parsed.status, sort_by=parsed.sort)
            for t in tasks:
                print(f"[{t.id}] {t.title} (status: {t.status}, priority: {t.priority.value}, tags: {t.tags})")
            return 0

        elif parsed.command == "update":
            tasks = storage.load_all()
            target = next((t for t in tasks if t.id == parsed.target_id), None)
            if not target:
                print(f"Error: Task with id {parsed.target_id} not found", file=sys.stderr)
                return 1
            if parsed.status:
                target.status = parsed.status
            if parsed.priority:
                target.priority = Priority(parsed.priority)
            storage.save_all(tasks)
            print(f"Task {target.id} updated")
            return 0

        elif parsed.command == "delete":
            tasks = storage.load_all()
            new_tasks = [t for t in tasks if t.id != parsed.target_id]
            if len(new_tasks) == len(tasks):
                print(f"Error: Task with id {parsed.target_id} not found", file=sys.stderr)
                return 1
            storage.save_all(new_tasks)
            print(f"Task {parsed.target_id} deleted")
            return 0

    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
