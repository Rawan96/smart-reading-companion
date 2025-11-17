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
        if pages <= 0:
         raise ValueError("pages must be positive")

        book = next((b for b in self.books if b.title == book_title), None)
        if book is None:
            return False


        today_str = datetime.now().strftime("%Y-%m-%d")

        for session in book.reading_sessions:
            if session['date'] == today_str:
                session['pages'] += pages
                break

        else:
            book.reading_sessions.append({"date": today_str, "pages": pages})

        book.add_pages(pages)
        if book.pages_read > book.total_pages:
            book.pages_read = book.total_pages


        self.reading_log.append({
            "book": book_title,
            "pages": pages,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

        return True


    def total_books(self):
        return len(self.books)

    def completed_books(self):
        finished_books = []
        for book in self.books:
            if book.pages_read == book.total_pages:
                finished_books.append(book)
        return finished_books
