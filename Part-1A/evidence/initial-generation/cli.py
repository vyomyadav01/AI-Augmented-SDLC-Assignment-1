import argparse
from .storage import TaskStorage
from .models import Priority, Status

def main():
    parser = argparse.ArgumentParser(description="Smart Todo CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title", type=str)
    add_parser.add_argument("--tags", type=str, default="")
    add_parser.add_argument("--priority", choices=["low", "med", "high"], default="low")

    args = parser.parse_args()
    storage = TaskStorage()

    if args.command == "add":
        tasks = storage.load_tasks()
        new_id = len(tasks) + 1
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        new_task = Task(id=new_id, title=args.title, tags=tags, priority=Priority(args.priority))
        tasks.append(new_task)
        storage.save_tasks(tasks)
        print(f"Task {new_id} added successfully.")
        exit(0)

if __name__ == "__main__":
    main()
