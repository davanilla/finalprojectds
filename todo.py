from datetime import datetime
import heapq

class Task:
    def __init__(self, title, deadline_str, priority, category="General"):
        self.title = title
        self.deadline = datetime.strptime(deadline_str, "%Y.%m.%d %H:%M")
        self.priority = priority
        self.category = category

    def __repr__(self):
        return f"Task(title={self.title}, deadline={self.deadline}, priority={self.priority}, category={self.category})"

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.deadline < other.deadline
        return self.priority < other.priority

if __name__ == "__main__":
    tasks = [
        Task("Finish math homework", "2025.05.20 18:00", 2, "School"),
        Task("Buy groceries", "2025.05.20 12:00", 3, "Personal"),
        Task("Call mom", "2025.05.20 10:00", 1, "Family"),
        Task("Call dad", "2025.05.20 10:30", 3, "Family")
    ]

    task_heap = []
    for task in tasks:
        heapq.heappush(task_heap, task)

    print("Tasks in priority order:")

    while task_heap:
        print(heapq.heappop(task_heap))