import os
import json
from datetime import datetime
from models.book import Book
from models.goal import Goal


from werkzeug.security import generate_password_hash, check_password_hash

BOOKS_FILE = "users.json"

class Reader:
    def __init__(self,  name, email, password_hash=None, books=None,reading_log=None, goals=None):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.books = books if books else []
        self.reading_log = reading_log if reading_log else []
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
                    reading_log=u.get("reading_log", []),
                    goals=u.get("goals", [])
                    )
        return None

    def save_reader(self):
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        for u in users:
            if u.get("email") == self.email:
                u["name"] = self.name
                u["password"] = self.password_hash
                u["books"] = [b.to_dict() for b in self.books]
                u["reading_log"] = self.reading_log
                u["goals"] = [g.to_dict() for g in self.goals]
                break
        else:
            users.append({
                "name": self.name,
                "email": self.email,
                "password": self.password_hash,
                "books": [b.to_dict() for b in self.books],
                "reading_log": self.reading_log,
                "goals": [g.to_dict() for g in self.goals]
            })

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)


    def add_goal(self, title, goal_type, target_value, deadline=None):
        goal = Goal(
            title=title,
            goal_type=goal_type,
            target_value=target_value,
            deadline=deadline,
            progress=0,
            completed=False,
            completed_at=None
        )

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

    def edit_goal_by_id(self, goal_id, title=None, goal_type=None, target_value=None, deadline=None, progress=None):
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
        goal.update_completion()
        self.save_reader()
        return True




    def load_books(self):
        try:
            with open(BOOKS_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book.from_dict(b) for b in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self):
        with open(BOOKS_FILE, "w") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4)

    def add_book(self, title, author, total_pages, genre):
        if any(b.title == title for b in self.books):
            return False
        new_book = Book(title, author, total_pages, genre)
        self.books.append(new_book)
        self.save_books()
        return True

    def find_book(self, title):
        return next((b for b in self.books if b.title == title), None)

    def delete_book(self, title):
        self.books = [b for b in self.books if b.title != title]
        self.save_books()

    def log_reading(self, title, pages):
        if pages <= 0:
            raise ValueError("Pages must be positive")

        book = self.find_book(title)
        if not book:
            return False


        book.add_pages(pages)

        self.reading_log.append({
            "book": title,
            "pages": pages,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self.save_books()
        return True



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
                    reading_log=u.get("reading_log", []),
                    goals=u.get("goals", [])
                )
        return None
