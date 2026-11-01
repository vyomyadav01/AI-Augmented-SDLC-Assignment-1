import pytest
from src.cli import main
from src.models import Priority, Task
from src.storage import TaskStorage


def test_ac1_empty_title_rejection():
    with pytest.raises(ValueError):
        Task(id=1, title="   ")

def test_ac2_filter_by_tag_and_status(tmp_path):
    db_file = tmp_path / "tasks.json"
    storage = TaskStorage(str(db_file))
    t1 = Task(id=1, title="T1", tags=["work"], status="pending")
    t2 = Task(id=2, title="T2", tags=["work"], status="done")
    storage.save_all([t1, t2])
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
    ret = main(["delete", "999", "--db", str(db_file)])
    assert ret == 1
