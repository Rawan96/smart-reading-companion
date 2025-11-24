import os
import json
from datetime import datetime
from models.book import Book
from models.goal import Goal


from werkzeug.security import generate_password_hash, check_password_hash

BOOKS_FILE = "users.json"

class Reader:
    def __init__(self,  name, email, password_hash=None, books=None, goals=None):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.books = books if books else []
        self.goals = [Goal.from_dict(g) for g in (goals or [])]


    @classmethod
    def create_user(cls, name, email, password):
        if cls.find_by_email(email):
            return None
        password_hash = generate_password_hash(password)
        reader = cls(name, email, password_hash)
        reader.save_reader()
        return reader

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def find_by_email(email):
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []
        for u in users:
            if u.get("email") == email:
                return Reader(
                    name=u["name"],
                    email=u["email"],
                    password_hash=u.get("password"),
                    books=[Book.from_dict(b) for b in u.get("books", [])],
                    goals=u.get("goals", [])
                    )
        return None


    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email.lower(),
            "password": self.password_hash,
            "books": [b.to_dict() for b in self.books],
            "goals": [g.to_dict() for g in self.goals]
        }

    def save_reader(self):
        try:
            with open(BOOKS_FILE, "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        for i, u in enumerate(users):
            if u.get("email") == self.email:
                users[i] = self.to_dict()
                break
        else:
            users.append(self.to_dict())

        with open(BOOKS_FILE, "w") as f:
            json.dump(users, f, indent=4)


    def add_goal(self, title,unit, goal_type, target_value, deadline=None ):
        goal = Goal(
            title=title,
            unit=unit,
            goal_type=goal_type,
            target_value=target_value,
            deadline=deadline,
            progress=0,
            completed=False,
            completed_at=None,
        )
        deadline = deadline or Goal.default_deadline(goal_type)
        goal.update_completion()

        self.goals.append(goal)
        self.save_reader()

    def find_goal_by_id(self, goal_id):
        return next((g for g in self.goals if getattr(g, "id", None) == goal_id), None)

    def delete_goal_by_id(self, goal_id):
        goal = self.find_goal_by_id(goal_id)
        if not goal:
            return False
        self.goals.remove(goal)
        self.save_reader()
        return True

    def edit_goal_by_id(self, goal_id, title=None, goal_type=None, target_value=None, deadline=None, progress=None,unit=None):
        goal = self.find_goal_by_id(goal_id)
        if not goal:
            return False
        if title is not None:
            goal.title = title
        if goal_type is not None:
            goal.goal_type = goal_type
        if target_value is not None:
            goal.target_value = target_value
            if goal.progress > goal.target_value:
                goal.progress = goal.target_value
        if deadline is not None:
            goal.deadline = deadline
        if progress is not None:
            goal.progress = progress
        if unit is not None:
            goal.unit = unit
        goal.update_completion()
        self.save_reader()
        return True

    def add_book(self, book: Book):
        if any(b.title == book.title for b in self.books):
            return False
        self.books.append(book)
        self.save_reader()
        return True

    def find_book(self, title):
        return next((b for b in self.books if b.title == title), None)

    def delete_book(self, title):
        self.books = [b for b in self.books if b.title != title]
        self.save_reader()


    @staticmethod
    def load_reader(email):
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        for u in users:
            if u.get("email") == email:
                return Reader(
                    name=u["name"],
                    email=u["email"],
                    password_hash=u.get("password"),
                    books=[Book.from_dict(b) for b in u.get("books", [])],
                    goals=u.get("goals", [])
                )
        return None
