from datetime import datetime
import heapq

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
        task = Task(name, deadline_str, priority, category)
        tasks.append(task)
        print(f"Added: {task}\n") 
    return tasks

if __name__ == "__main__":
    user_tasks = get_user_input()
    schedule_tasks(user_tasks)
    