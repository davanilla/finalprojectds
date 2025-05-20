from datetime import datetime
from plyer import notification
import time
import heapq
import json

class Task:
    def __init__(self, name, deadline_str, priority, category="General"):
        self.name = name
        self.deadline = datetime.strptime(deadline_str, "%Y.%m.%d %H:%M")
        self.priority = priority
        self.category = category

    def __repr__(self):
        return f"Task(name={self.name}, deadline={self.deadline}, priority={self.priority}, category={self.category})"

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.deadline < other.deadline
        return self.priority < other.priority

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
        deadline_str = input("Deadline (YYYY.MM.DD HH:MM): ")
        priority = int(input("Priority (1 to 100): "))
        category = input("Category (default = 'General'): ")
        if not category:
            category = "General"
        task = Task(name, deadline_str, priority, category)
        tasks.append(task)
        print(f"Added: {task}\n") 
    return tasks

def save_tasks(tasks, filename="todolist.json"):
    tasks_data = []
    for t in tasks:
        tasks_data.append({
            "name": t.name,
            "deadline": t.deadline.strftime("%Y.%m.%d %H:%M"),
            "priority": t.priority,
            "category": t.category
        })
    with open(filename, "w") as f:
        json.dump(tasks_data, f, indent=2)
    print(f"Tasks saved to {filename}")

def load_tasks(filename="todolist.json"):
    tasks =[]
    try:
        with open(filename, "r") as f:
            tasks_data = json.load(f)
            for t in tasks_data:
                tasks.append(Task(t["name"], t["deadline"], t["priority"], t["category"]))
        print(f"Loaded {len(tasks)} tasks from {filename}")
    except FileNotFoundError:
        print("To-do list is void.")
    return tasks

def notify_task(task):
    notification.notify(
        title=f"Reminder: {task.name}",
        message=f"Deadline at {task.deadline.strftime('%H:%M')}, Priority: {task.priority}",
        timeout = 30
    )   
    
def notify_due_tasks(tasks):
    now = datetime.now()
    for t in tasks:
        if 0 <= (t.deadline - now).total_seconds() <= 3600:
            notify_task(t)

if __name__ == "__main__":
    tasks = load_tasks()
    new_tasks = get_user_input()
    tasks.extend(new_tasks)
    save_tasks(tasks)
    schedule_tasks(tasks)
    notify_due_tasks(tasks)
    