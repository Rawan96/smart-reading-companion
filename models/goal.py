from datetime import date
import uuid


class Goal:
    def __init__(self, title, goal_type, target_value, deadline=None, progress=0, completed=False, completed_at=None,goal_id=None):
        self.id = goal_id or str(uuid.uuid4())
        self.title = title
        self.goal_type = goal_type
        self.target_value = target_value
        self.deadline = deadline
        self.progress = progress
        self.completed = completed
        self.completed_at = completed_at

    def update_progress(self, amount):
        self.progress += amount
        if self.progress >= self.target_value:
            self.progress = self.target_value
            self.completed = True

    def update_completion(self):
        if self.progress >= self.target_value:
            self.completed = True
            if not self.completed_at:
                self.completed_at = date.today().isoformat()
        else:
            self.completed = False
            self.completed_at = None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "goal_type": self.goal_type,
            "target_value": self.target_value,
            "deadline": self.deadline,
            "progress": self.progress,
            "completed": self.completed,
            "completed_at": self.completed_at,
        }

    @staticmethod
    def from_dict(data):
        return Goal(
            title=data["title"],
            goal_type=data["goal_type"],
            target_value=data["target_value"],
            deadline=data.get("deadline"),
            progress=data.get("progress", 0),
            completed=data.get("completed", False),
            completed_at=data.get("completed_at"),
            goal_id=data.get("id")
        )
