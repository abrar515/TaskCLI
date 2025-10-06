import sys
import json
from datetime import datetime


def main():


# Basic command line argument parsing
    if len(sys.argv) < 2:
        print("Available commands: add, list, delete, update, mark' OR mark-<status> <id>")
        sys.exit()


# Load existing tasks from tasks.json
    try:
        with open('tasks.json', 'r') as f:
            tasks = f.read().strip()
            tasks = json.loads(tasks) if tasks else [] 
    except FileNotFoundError:
        tasks = []
    except json.JSONDecodeError:
        print("Warning: tasks.json contains invalid JSON; starting with empty task list.")
        tasks = []
    
# track whether we changed tasks and only write when needed
    dirty = False
    

# Determine command line arguments
    cmd = sys.argv[1].lower()
    if not (cmd in ['add', 'list', 'delete', 'update'] or cmd == 'mark' or cmd.startswith('mark-')):
        print("Unknown command. Available commands: add, list, delete, update, mark <id> <status>, mark-<status> <id>")
        sys.exit(1)


# Add a new task
    if cmd == 'add':
        try:
            description = " ".join(sys.argv[2:]).strip()
            tasks = add_task(description, tasks)
            print(f"Added task {tasks[-1]['id']}: {tasks[-1]['description']}")
            dirty = True
        except IndexError:
            print("Usage: python TasksCLI.py add <task_description>")
            sys.exit()



# Update a task's description
                                
    elif cmd == 'update':
        try:
            task_id = int(sys.argv[2])
            description = " ".join(sys.argv[3:])
            tasks, changed = update_task(task_id, description, tasks)
            if changed:
                dirty = True
                print(f"Description of Task {task_id} updated to: {description}")
        except (IndexError, ValueError):
            print("Usage: python TasksCLI.py update <task_id> <new_description>")
            sys.exit()



# Delete a task
    elif cmd == 'delete':
        try:
            task_id = int(sys.argv[2])
            tasks, changed = delete_task(task_id, tasks)
            #print(f"tasks = {tasks}\n changed = {changed}")
            if changed:
                dirty = True
                print(f"Deleted task {task_id}. IDs renumbered.")
            else:
                print(f"Task {task_id} not found.")
        except (ValueError, IndexError):
            print("Usage: python TasksCLI.py delete <task_id>")
            sys.exit()



# Mark a task as todo, in-progress, or done
    elif cmd == 'mark' or cmd.startswith('mark-'):
        
        try:
            # support both: `mark <id> <status>` and `mark-<status> <id>`
            if cmd.startswith('mark-'):
                status = cmd.split('-', 1)[1]
                task_id = int(sys.argv[2])
            else:
                task_id = int(sys.argv[2])
                status = sys.argv[3].lower()
            if status not in ['todo', 'in-progress', 'done']:
                raise ValueError
            tasks, changed = mark_task(task_id, status, tasks)
            if changed:
                dirty = True
                print(f"Task {task_id} marked as {status}.")
            else:
                print(f"Task {task_id} not found.")
        except (ValueError, IndexError):
            print("Usage: python TasksCLI.py mark <task_id> <status>  OR  python TasksCLI.py mark-<status> <task_id>")
            print("Status must be one of: todo, in-progress, done")
            sys.exit()



# List tasks, optionally filtered by status
    elif cmd == 'list':
        print("\n============================================================================================================")
        print(f"{'id':>4} | {'description':30} | {'status':12} | {'createdAt':25} | {'updatedAt':25}")
        print("============================================================================================================")
        if len(sys.argv) == 2:
            list_tasks(tasks)
        elif len(sys.argv) == 3:
            status = sys.argv[2].lower()
            if status not in ['todo', 'in-progress', 'done']:
                print("Status must be one of: todo, in-progress, done")
                sys.exit()
            list_tasks_by_status(status, tasks)


    if dirty:
        write_tasks(tasks)
    




def add_task(description, tasks):
    new_id = max((t.get('id', 0) for t in tasks), default=0) + 1
    tasks.append({
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.utcnow().isoformat(),
        "updatedAt": datetime.utcnow().isoformat()
    })
    return tasks


def update_task(task_id, description, tasks):
    idx = find_task_index(task_id, tasks)
    if idx is None:
        print(f"Task {task_id} not found.")
        return tasks, False
    tasks[idx]['description'] = description
    tasks[idx]['updatedAt'] = datetime.utcnow().isoformat()
    return tasks, True

def delete_task(task_id, tasks):
    new_tasks = [task for task in tasks if task.get('id') != task_id]
    if len(new_tasks) == len(tasks):
        return None, False
    # renumber ids to be sequential
    for i, task in enumerate(new_tasks, start=1):
        task['id'] = i
    return new_tasks, True



# Marking a task as in progress or done
def mark_task(task_id, status, tasks):
    idx = find_task_index(task_id, tasks)
    if idx is None:
        return None, False
    tasks[idx]['status'] = status
    tasks[idx]['updatedAt'] = datetime.utcnow().isoformat()
    return tasks, True



def list_tasks(tasks):
    for task in tasks:
        print(f"{task['id']:>4} | {task['description'][:30]:30} | {task['status']:12} | {task['createdAt']:25} | {task['updatedAt']:25}")




def list_tasks_by_status(status, tasks):
    for task in tasks:
        if task['status'] == status:
            print(f"{task['id']:>4} | {task['description'][:30]:30} | {task['status']:12} | {task['createdAt']:25} | {task['updatedAt']:25}")



def write_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=2)



def find_task_index(task_id, tasks):
    for i, t in enumerate(tasks):
        if t.get('id') == task_id:
            return i
    return None


if __name__ == '__main__':
    main()