from datetime import datetime

class Task:
    def __init__(self, title, deadline_str, priority, category="General"):
        self.title = title
        self.deadline = datetime.strptime(deadline_str, "%Y.%m.%d %H:%M")
        self.priority = priority
        self.category = category
    def __repr__(self):
        return f"Task(title={self.title}, deadline={self.deadline}, priority={self.priority}, category={self.category})"