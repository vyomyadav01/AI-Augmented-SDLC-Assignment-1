import argparse
import sys

from src.storage import TaskStorage


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smart Todo CLI")
    parser.add_argument("command", nargs="?", choices=["add", "delete", "list"])
    parser.add_argument("target_id", nargs="?", type=int)
    parser.add_argument("--db", default="tasks.json")
    parsed = parser.parse_args(args)

    storage = TaskStorage(parsed.db)
    if parsed.command == "delete" and parsed.target_id:
        tasks = storage.load_all()
        new_tasks = [t for t in tasks if t.id != parsed.target_id]
        if len(new_tasks) == len(tasks):
            return 1
        storage.save_all(new_tasks)
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
