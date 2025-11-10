from collections import Counter

class Analytics:
    def __init__(self, reader):
        self.reader = reader


    def total_pages_read(self):
        return sum(book.pages_read for book in self.reader.books)

    def average_pages_per_day(self):
        log = self.reader.reading_log
        if not log:
            return 0
        dates = [entry['date'].split(' ')[0] for entry in log]
        total_pages = sum(entry['pages'] for entry in log)
        return round(total_pages / len(dates), 2)

    def genre_distribution(self):
        return dict(Counter(b.genre for b in self.reader.books))

    def completion_rate(self):
        books = self.reader.books
        if not books:
            return 0

        completed = sum(b.pages_read == b.total_pages for b in books)
        return round((completed / len(books)) * 100, 2)
