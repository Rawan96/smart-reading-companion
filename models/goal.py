import calendar
from datetime import date, datetime, timedelta
import uuid


class Goal:
    def __init__(self, title,unit, goal_type, target_value, deadline=None, progress=0, completed=False, completed_at=None,goal_id=None):
        self.id = goal_id or str(uuid.uuid4())
        self.title = title
        self.unit = unit
        self.goal_type = goal_type
        self.target_value = target_value
        self.deadline = deadline
        self.progress = progress
        self.completed = completed
        self.completed_at = completed_at


    def update_completion(self):
        if self.progress >= self.target_value:
            self.completed = True
            if not self.completed_at:
               self.completed_at = datetime.now().strftime("%Y-%m-%d")
        else:
            self.completed = False
            self.completed_at = None


    @staticmethod
    def default_deadline(goal_type: str):
        today = date.today()
        if goal_type == "Daily":
            return today.isoformat()
        elif goal_type == "Weekly":
            return (today + timedelta(days=7)).isoformat()
        elif goal_type == "Monthly":
            month = today.month + 1
            year = today.year
            if month > 12:
                month = 1
                year += 1
            day = min(today.day, calendar.monthrange(year, month)[1])
            return date(year, month, day).isoformat()
        elif goal_type == "Annual":
            return date(today.year + 1, today.month, today.day).isoformat()
        return None


    def to_dict(self):
        return {
        "id": str(self.id),
        "title": str(self.title or ""),
        "goal_type": str(self.goal_type or ""),
        "target_value": int(self.target_value or 0),
        "deadline": str(self.deadline or ""),
        "progress": int(self.progress or 0),
        "unit": str(self.unit or "books"),
        "completed": bool(self.completed),
        "completed_at": str(self.completed_at or "")
        }

    @staticmethod
    def from_dict(data):
        return Goal(
            title=data["title"],
            unit=data.get("unit", "books"),
            goal_type=data["goal_type"],
            target_value=data["target_value"],
            deadline=data.get("deadline"),
            progress=data.get("progress", 0),
            completed=data.get("completed", False),
            completed_at=data.get("completed_at"),
            goal_id=data.get("id"),
        )
