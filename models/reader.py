from datetime import datetime

class Reader:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.reading_log = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, title):
        self.books = [book for book in self.books if book.title != title]


    def log_reading(self, book_title, pages):
        book = None
        for b in self.books:
            if b.title == book_title:
                book = b
                break

        if book:
            book.add_pages(pages)
            book.reading_sessions.append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "pages": pages
            })

            self.reading_log.append({
                "book":book_title,
                "pages":pages,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

    def total_books(self):
        return len(self.books)

    def completed_books(self):
        finished_books = []
        for book in self.books:
            if book.pages_read == book.total_pages:
                finished_books.append(book)
        return finished_books
