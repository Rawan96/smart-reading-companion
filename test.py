# Create a reader
from models.reader import Reader
from models.analytics import Analytics
from models.book import Book


reader = Reader("Rawan")

reader.add_book(Book("Deep Work", "Cal Newport", 304, "Productivity"))
reader.add_book(Book("Atomic Habits", "James Clear", 250, "Self-Help"))
reader.add_book(Book("1984", "George Orwell", 328, "Fiction"))

reader.log_reading("Deep Work", 50)
reader.log_reading("Atomic Habits", 100)
reader.log_reading("1984", 200)
reader.log_reading("1984", 128)

analytics = Analytics(reader)

print("Total Pages Read:", analytics.total_pages_read())
print("Average Pages Per Day:", analytics.average_pages_per_day())
print("Genre Distribution:", analytics.genre_distribution())
print("Completion Rate:", analytics.completion_rate(), "%")

print("\nCompleted Books:", [b.title for b in reader.completed_books()])
