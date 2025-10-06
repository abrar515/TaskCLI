# TaskCLI - Command Line Task Manager

TaskCLI is a Python-based command-line tool for managing tasks directly from your terminal. It allows you to add, list, update, delete, and mark tasks, storing them locally in a JSON file along with timestamps for creation and updates.

## Project Structure

```
├── taskCLI.py              # Main CLI tool implementation
├── test_taskcli_pytest.py  # Unit tests using pytest
└── tasks.json              # (auto-generated) stores tasks data
```

## Features

- Add tasks with a description  
- List tasks, with optional filtering by status  
- Update task descriptions  
- Delete tasks by ID, with automatic renumbering  
- Mark tasks as "todo", "in-progress", or "done"  
- Automatic timestamping for creation and updates  

## Installation

Ensure that Python 3.8 or later is installed on your system.

```bash
git clone https://github.com/abrar515/TaskCLI/
cd taskcli
pip install -r requirements.txt   # optional, not required for basic usage
```

## Usage

### 1. Add a task

```bash
python taskCLI.py add "Finish project report"
```

Output:
```
Added task 1: Finish project report
```

### 2. List all tasks

```bash
python taskCLI.py list
```

Output:
```
  id | description                   | status       | createdAt                | updatedAt
============================================================================================================
   1 | Finish project report        | todo         | 2025-10-06T14:30:00      | 2025-10-06T14:30:00
```

### 3. Filter tasks by status

```bash
python taskCLI.py list done
```

### 4. Update a task description

```bash
python taskCLI.py update 1 "Finish final project report"
```

Output:
```
Description of Task 1 updated to: Finish final project report
```

### 5. Delete a task

```bash
python taskCLI.py delete 1
```

Output:
```
Deleted task 1. IDs renumbered.
```

### 6. Mark a task

```bash
python taskCLI.py mark 1 done
# or
python taskCLI.py mark-done 1
```

Output:
```
Task 1 marked as done.
```

## Running Tests

The project includes a pytest test suite (`test_taskcli_pytest.py`) that verifies the main functionalities.

To run tests:

```bash
pytest -v
```

Tests cover:
- Task creation and ID assignment  
- Description updates and timestamp handling  
- Task deletion and ID renumbering  
- Status updates  
- Task lookup behavior  

## Data Storage

All tasks are stored in a `tasks.json` file in the same directory as the script. Example structure:

```json
[
  {
    "id": 1,
    "description": "Finish project report",
    "status": "todo",
    "createdAt": "2025-10-06T14:30:00",
    "updatedAt": "2025-10-06T14:30:00"
  }
]
```

## Future Improvements

- Add priority levels for tasks  
- Add due dates and reminders  
- Support exporting tasks to CSV or Markdown  
- Optional integration with calendar tools  


## Project Source

This project is based on the [Task Tracker project on roadmap.sh](https://roadmap.sh/projects/task-tracker).


## Author

Abrar Ahmad  
Email: abrar515@hotmail.com
