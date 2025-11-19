from datetime import date, datetime

class Book:
    def __init__(self, title, author, total_pages, pages_read=0, notes=None, quotes=None, reading_sessions=None, cover=None, status="to-read",current_page=0):
        self.title = title
        self.author = author
        self.total_pages = total_pages
        self.pages_read = pages_read
        self.status = status
        self.current_page = current_page
        self.cover = cover
        self.notes = notes or []
        self.quotes = quotes or []
        self.reading_sessions = reading_sessions or []


    def add_pages(self, pages):
        pages = int(pages)

        max_allowed = self.total_pages - self.pages_read
        pages = min(pages, max_allowed)

        if pages <= 0:
            return

        self.pages_read += pages
        self.current_page = self.pages_read

        self.reading_sessions.append({
            "pages": pages,
            "date": str(date.today())
        })

    def set_current_page(self, page, reader=None):
        if page < 0:
            page = 0
        if page > self.total_pages:
            page = self.total_pages

        pages_added = max(0, page - self.pages_read)

        self.current_page = page
        if self.status != "to-read":
            self.pages_read = max(self.pages_read, page)
        else:
            self.pages_read = 0

        if pages_added > 0:
            today_str = str(date.today())
            for session in self.reading_sessions:
                if session["date"] == today_str:
                    session["pages"] += pages_added
                    break
            else:
                self.reading_sessions.append({"date": today_str, "pages": pages_added})

            if reader:
                reader.reading_log.append({
                    "book": self.title,
                    "pages": pages_added,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

    def add_note(self, text):
        self.notes.append(text)

    def add_quote(self, text):
        self.quotes.append(text)

    def progress_percentage(self):
        if self.total_pages == 0:
            return 0
        return round((self.pages_read / self.total_pages) * 100, 1)

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "total_pages": self.total_pages,
            "cover": self.cover,
            "pages_read": self.pages_read,
            "status": self.status,
            "current_page": self.current_page,
            "notes": self.notes,
            "quotes": self.quotes,
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
            notes=data.get("notes", []),
            quotes=data.get("quotes", []),
            reading_sessions=data.get("reading_sessions", [])
        )
