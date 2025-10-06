import pytest
from datetime import datetime
import taskCLI


@pytest.fixture
def empty_tasks():
    return []


def test_add_task_assigns_id_and_timestamps(empty_tasks):
    tasks = taskCLI.add_task('Test task', empty_tasks)
    assert len(tasks) == 1
    t = tasks[0]
    assert t['id'] == 1
    assert t['description'] == 'Test task'
    assert t['status'] == 'todo'
    # parseable timestamps
    datetime.fromisoformat(t['createdAt'])
    datetime.fromisoformat(t['updatedAt'])


def test_update_task_changes_description_and_timestamp(empty_tasks):
    tasks = taskCLI.add_task('Old', empty_tasks)
    tasks, changed = taskCLI.update_task(1, 'New', tasks)
    assert changed == True
    assert tasks[0]['description'] == 'New'
    datetime.fromisoformat(tasks[0]['updatedAt'])


def test_delete_task_removes_and_renumbers(empty_tasks):
    tasks = empty_tasks
    for i in range(3):
        tasks = taskCLI.add_task(f'T{i}', tasks)
    new_tasks, changed = taskCLI.delete_task(2, tasks)
    assert changed == True
    assert len(new_tasks) == 2
    assert [t['id'] for t in new_tasks] == [1, 2]


def test_mark_task_updates_status(empty_tasks):
    tasks = taskCLI.add_task('X', empty_tasks)
    tasks, changed = taskCLI.mark_task(1, 'in-progress', tasks)
    assert changed ==  True
    assert tasks[0]['status'] == 'in-progress'


def test_find_task_index_returns_none_for_missing():
    tasks = [{'id': 1}, {'id': 2}]
    assert taskCLI.find_task_index(999, tasks) is None
    assert taskCLI.find_task_index(2, tasks) == 1
