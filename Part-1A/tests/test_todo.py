import pytest
from src.cli import main
from src.models import Priority, Task
from src.storage import TaskStorage


def test_ac1_task_saved_with_pending_status(tmp_path):
    db_file = tmp_path / "tasks.json"
    ret = main(["--db", str(db_file), "add", "Submit assignment", "--priority", "high", "--tags", "wilp,mtech"])
    assert ret == 0

    storage = TaskStorage(str(db_file))
    tasks = storage.load_all()
    assert len(tasks) == 1
    assert tasks[0].id == 1
    assert tasks[0].title == "Submit assignment"
    assert tasks[0].status == "pending"
    assert tasks[0].priority == Priority.HIGH
    assert tasks[0].tags == ["wilp", "mtech"]


def test_ac2_filter_by_tag_and_status(tmp_path):
    db_file = tmp_path / "tasks.json"
    storage = TaskStorage(str(db_file))
    t1 = Task(id=1, title="T1", tags=["work"], status="pending")
    t2 = Task(id=2, title="T2", tags=["work"], status="done")
    t3 = Task(id=3, title="T3", tags=["personal"], status="done")
    storage.save_all([t1, t2, t3])

    filtered = storage.list_tasks(tag="work", status="done")
    assert len(filtered) == 1
    assert filtered[0].id == 2


def test_ac3_priority_sorting(tmp_path):
    db_file = tmp_path / "tasks.json"
    storage = TaskStorage(str(db_file))
    t_low = Task(id=1, title="Low", priority=Priority.LOW)
    t_high = Task(id=2, title="High", priority=Priority.HIGH)
    t_med = Task(id=3, title="Med", priority=Priority.MED)
    storage.save_all([t_low, t_high, t_med])

    sorted_tasks = storage.list_tasks(sort_by="priority")
    assert [t.priority for t in sorted_tasks] == [Priority.HIGH, Priority.MED, Priority.LOW]


def test_ac4_invalid_id_exit_code(tmp_path):
    db_file = tmp_path / "tasks.json"
    ret_update = main(["--db", str(db_file), "update", "999", "--status", "done"])
    assert ret_update == 1

    ret_delete = main(["--db", str(db_file), "delete", "999"])
    assert ret_delete == 1


def test_validation_empty_title_rejection():
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Task(id=1, title="   ")
