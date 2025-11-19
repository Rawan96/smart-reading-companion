from collections import  defaultdict
import datetime

class Analytics:
    def __init__(self, reader):
        self.reader = reader

    def total_books(self):
        return len(self.reader.books)

    def total_pages_read(self):
        return sum(b.pages_read for b in self.reader.books)

    def completion_rate(self):
        books = self.reader.books
        total = len(books)
        if total == 0:
            return 0
        completed = sum(1 for b in books if b.pages_read >= b.total_pages)
        return round((completed / total) * 100)

    def average_books_monthly(self):

        completed_books = []
        for b in self.reader.books:
            if b.pages_read >= b.total_pages:
                last_session_date = b.reading_sessions[-1]["date"]
                last_session_date = datetime.strptime(last_session_date, "%Y-%m-%d")
                completed_books.append(last_session_date)

        if not completed_books:
            return 0

        months = defaultdict(int)
        for d in completed_books:
            month_key = d.strftime("%Y-%m")
            months[month_key] += 1

        total_months = len(months)
        total_books = sum(months.values())
        return round(total_books / total_months)
