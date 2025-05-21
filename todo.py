from datetime import datetime
from plyer import notification
import time
import json

DATA_FILE = "todolist.json"
DATE_FORMAT = "%Y.%m.%d %H:%M"

class Task:
    def __init__(self, name, deadline_str, priority):
        self.name = name
        self.deadline = datetime.strptime(deadline_str, DATE_FORMAT)
        self.priority = priority

    def __repr__(self):
        return f"{self.name} (Deadline: {self.deadline.strftime(DATE_FORMAT)}, Priority: {self.priority})"


    def __lt__(self, other):
        if self.priority == other.priority:
            return self.deadline < other.deadline
        return self.priority < other.priority
    
    def __eq__(self, other):
        return (
            isinstance(other, Task) and
            self.name == other.name and
            self.deadline == other.deadline and
            self.priority == other.priority
        )
    
class MinHeap:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)
        self._heapify_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            return None
        if len(self.data) == 1:
            return self.data.pop()
        root = self.data[0]
        self.data[0] = self.data.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, idx):
        parent = (idx - 1) // 2
        if idx > 0 and self.data[idx] < self.data[parent]:
            self.data[idx], self.data[parent] = self.data[parent], self.data[idx]
            self._heapify_up(parent)

    def _heapify_down(self, idx):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        if left < len(self.data) and self.data[left] < self.data[smallest]:
            smallest = left
        if right < len(self.data) and self.data[right] < self.data[smallest]:
            smallest = right
        if smallest != idx:
            self.data[idx], self.data[smallest] = self.data[smallest], self.data[idx]
            self._heapify_down(smallest)

    def is_empty(self):
        return len(self.data) == 0


def schedule_tasks(tasks):
    if not tasks:
        print("There is void instead of a list!")
        return
    temp_heap = MinHeap()
    for task in tasks:
        temp_heap.push(task)

    print("To-do list:")
    
    while not temp_heap.is_empty():
        task = temp_heap.pop()
        print(task)

def get_user_input():
    name = input("Task name: ")
    
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
            if 1 <= priority <= 100:
                break
            else: 
                print("1 TO 100 PLEASE^^")
        except ValueError:
            print("Enter a NUMBER^^")

    task = Task(name, deadline_str, priority)
    print(f"Added: {task}\n") 
    return task

def save_tasks(tasks, filename=DATA_FILE):
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            "name": task.name,
            "deadline": task.deadline.strftime(DATE_FORMAT),
            "priority": task.priority
        })
    with open(filename, "w") as f:
        json.dump(tasks_data, f, indent=2)
    print(f"Task(s) saved to {filename}")

def load_tasks(filename=DATA_FILE):
    tasks =[]
    try:
        with open(filename, "r") as f:
            tasks_data = json.load(f)
            for task in tasks_data:
                tasks.append(Task(task["name"], task["deadline"], task["priority"]))
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

def remove_task(tasks):
    if not tasks:
        print("Void cannot be removed.")
        return tasks

    print("Tasks:")
    for idx, task in enumerate(tasks, 1):
        print(f"{idx}. {task.name} (Deadline: {task.deadline.strftime(DATE_FORMAT)}, Priority: {task.priority})")

    try:
        choice = int(input("Enter the task number to remove: "))
        if 1 <= choice <= len(tasks):
            removed = tasks.pop(choice - 1)
            print(f"Removed task: {removed.name}")
        else:
            print("Wrong number^^")
    except ValueError:
        print("Tru again^^")
    
    return tasks


def show_menu():
    print("\nChoose an option:")
    print("1. Add a task")
    print("2. List tasks")
    print("3. Remove task")
    print("4. Start reminder loop")
    print("5. Clear all tasks")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ")
    return choice.strip()

def run_todo():
    tasks = load_tasks()
    while True:
        choice = show_menu()
        if choice == '1':
            task = get_user_input()
            if task not in tasks:
                tasks.append(task)
                save_tasks(tasks)
            else:
                print("This task already exists!")
        elif choice == '2':
            schedule_tasks(tasks)
        
        elif choice == '3':
            tasks = remove_task(tasks)
        
        elif choice == '4':
            continuous_notifs(tasks)
        
        elif choice == '5':
            confirm = input("Are you ready to face the void? (yes/no): ").lower()
            if confirm == 'yes':
                tasks.clear()
                print("Embrace the void!")
            else:
                print("The void will await for your return.")

        elif choice == '6':
            save_tasks(tasks)
            print("Goodbye!")
            break
        
        else:
            print("Select 1-6^^")

if __name__ == "__main__":
    run_todo()
    