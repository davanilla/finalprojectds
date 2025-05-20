from datetime import datetime
from plyer import notification
import time
import heapq
import json

DATA_FILE = "todolist.json"
DATE_FORMAT = "%Y.%m.%d %H:%M"

class Task:
    def __init__(self, name, deadline_str, priority, category="General"):
        self.name = name
        self.deadline = datetime.strptime(deadline_str, DATE_FORMAT)
        self.priority = priority
        self.category = category

    def __repr__(self):
        return f"Task(name={self.name}, deadline={self.deadline}, priority={self.priority}, category={self.category})"

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.deadline < other.deadline
        return self.priority < other.priority
    
    def __eq__(self, other):
        return (
            isinstance(other, Task) and
            self.name == other.name and
            self.deadline == other.deadline and
            self.priority == other.priority and
            self.category == other.category
        )

def schedule_tasks(tasks):
    task_heap = []
    for task in tasks:
        heapq.heappush(task_heap, task)

    print("To-do list:")
    while task_heap:
        task = heapq.heappop(task_heap)
        print(task)

def get_user_input():
    tasks = []
    print("Enter your task (type 'done' when done): ")
    while True:
        name = input("Task: ")
        if name.lower() == 'done':
            break
        while True: 
            deadline_str = input("Deadline (YYYY.MM.DD HH:MM): ").strip()
            try: 
                deadline = datetime.strptime(deadline_str, DATE_FORMAT)
                if deadline < datetime.now():
                    print("Deadline must be in the future, you lazy one^^")
                else:
                    break
            except ValueError:
                print("Invalid date. Try again with your eyes open^^")
        while True:
            try:
                priority = int(input("Priority (1 to 100): ").strip())
                if (1 <= priority <= 100):
                    break
                else: 
                    print("1 TO 100 PLEASE^^")
            except ValueError:
                print("Enter a NUMBER^^")

        category = input("Category (default = 'General'): ")
        if not category:
            category = "General"

        task = Task(name, deadline_str, priority, category)
        tasks.append(task)
        print(f"Added: {task}\n") 
    return tasks

def save_tasks(tasks, filename=DATA_FILE):
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            "name": task.name,
            "deadline": task.deadline.strftime(DATE_FORMAT),
            "priority": task.priority,
            "category": task.category
        })
    with open(filename, "w") as f:
        json.dump(tasks_data, f, indent=2)
    print(f"Tasks saved to {filename}")

def load_tasks(filename="todolist.json"):
    tasks =[]
    try:
        with open(filename, "r") as f:
            tasks_data = json.load(f)
            for task in tasks_data:
                tasks.append(Task(task["name"], task["deadline"], task["priority"], task["category"]))
        print(f"Loaded {len(tasks)} tasks from {filename}")
    except FileNotFoundError:
        print("To-do list is void.")
    return tasks

def notify_task(task):
    try:
        notification.notify(
            title=f"Reminder: {task.name}",
            message=f"Deadline at {task.deadline.strftime('%H:%M')}, Priority: {task.priority}",
            timeout=30
        )
    except NotImplementedError:
        print(f"[!] Notification failed: No system notifier found. Skipping notification for '{task.name}'.")
   
    
def notify_due_tasks(tasks):
    now = datetime.now()
    for task in tasks:
        if 0 <= (task.deadline - now).total_seconds() <= 3600:
            notify_task(task)

def continuous_notifs(tasks):
    print("I'm gonna remind you of relevant tasks every 5 minutes. Ctrl+C to abort.")
    try:
        while True:
            notify_due_tasks(tasks)
            time.sleep(300)
    except KeyboardInterrupt:
        print("Mission aborted.")

def run_todo():
    tasks = load_tasks()
    new_tasks = get_user_input()
    tasks.extend(new_tasks)
    save_tasks(tasks)
    schedule_tasks(tasks)
    notify_due_tasks(tasks)
    continuous_notifs(tasks)

if __name__ == "__main__":
    run_todo()
    