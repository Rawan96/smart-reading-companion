class Book:
    def __init__(self, title, author, total_pages,genre):
        self.title = title
        self.author = author
        self.total_pages = total_pages
        self.genre = genre
        self.pages_read = 0
        self.notes = []
        self.quotes = []
        self.reading_sessions = []


    def add_pages(self,pages):
        self.pages_read = min(self.total_pages, self.pages_read + pages)


    def progress_percentage(self):
        return round((self.pages_read / self.total_pages) * 100, 2) if self.total_pages else 0

    def add_note(self, text):
        self.notes.append(text)


    def add_quote(self, text):
        self.quotes.append(text)

    def mark_completed(self):
        self.pages_read = self.total_pages

    def __repr__(self):
        return f"<Book {self.title} ({self.progress_percentage()}%)>"
