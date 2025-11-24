from datetime import date, datetime

class Book:
    def __init__(self, title, author, total_pages, pages_read=0, reading_sessions=None, cover=None, status="to-read",current_page=0):
        self.title = title
        self.author = author
        self.total_pages = total_pages
        self.pages_read = pages_read
        self.status = status
        self.current_page = current_page
        self.cover = cover
        self.reading_sessions = reading_sessions or []


    def set_current_page(self, page, reader=None):
        if page < 0:
            page = 0
        if page > self.total_pages:
            page = self.total_pages

        old_pages = self.pages_read

        if page > old_pages:
            pages_to_add = page - old_pages
            today_str = str(date.today())
            for session in self.reading_sessions:
                if session["date"] == today_str:
                    session["pages"] += pages_to_add
                    break
            else:
                self.reading_sessions.append({"pages": pages_to_add, "date": today_str})

        elif page < old_pages:
            pages_to_remove = old_pages - page
            i = len(self.reading_sessions) - 1
            while pages_to_remove > 0 and i >= 0:
                session = self.reading_sessions[i]
                if session["pages"] <= pages_to_remove:
                    pages_to_remove -= session["pages"]
                    self.reading_sessions.pop(i)
                else:
                    session["pages"] -= pages_to_remove
                    pages_to_remove = 0
                i -= 1

        self.pages_read = page
        self.current_page = page

        if reader:
            reader.save_reader()

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "total_pages": self.total_pages,
            "cover": self.cover,
            "pages_read": self.pages_read,
            "status": self.status,
            "current_page": self.current_page,
            "reading_sessions": self.reading_sessions
        }

    @staticmethod
    def from_dict(data):
        """Create a Book instance from JSON data"""
        return Book(
            title=data["title"],
            author=data["author"],
            total_pages=data["total_pages"],
            cover = data.get("cover"),
            pages_read=data.get("pages_read", 0),
            status=data.get("status", "to-read"),
            current_page=data.get("current_page", 0),
            reading_sessions=data.get("reading_sessions", [])
        )
