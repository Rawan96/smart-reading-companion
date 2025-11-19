from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.helpers import load_reader
from utils.decorators import login_required
from models.book import Book
from models.analytics import Analytics
import os
from datetime import date

book_bp = Blueprint('book', __name__)


@book_bp.route('/add_book', methods=['POST'])
@login_required
def add_book():
    reader = load_reader()

    title = request.form.get("title")
    author = request.form.get("author")
    total_pages = int(request.form.get("total_pages") or 0)
    status = request.form.get("status", "to-read")
    current_page = int(request.form.get("current_page") or 0)
    cover_url = request.form.get("cover_url", "").strip()

    if any(b.title == title for b in reader.books):
        flash(f"Book '{title}' already exists!", "error")
        return redirect(url_for("library.library"))

    new_book = Book(title=title, author=author, total_pages=total_pages, cover=cover_url, status=status)

    if status == "reading":
        new_book.set_current_page(current_page, reader)
    elif status == "completed":
        new_book.set_current_page(total_pages, reader)

    reader.books.append(new_book)
    reader.save_reader()
    flash("Book added successfully!", "success")

    return redirect(url_for('library.library'))


@book_bp.route("/edit_book/<string:title>", methods=["GET", "POST"])
@login_required
def edit_book(title):
    reader = load_reader()
    book = reader.find_book(title)

    if not book:
        flash("Book not found!", "error")
        return redirect(url_for("library.library"))

    if request.method == "POST":
        try:
            new_status = request.form["status"]
            new_current_page = int(request.form.get("current_page", 0))
            total_pages = int(request.form["total_pages"])
        except ValueError:
            flash("Please enter valid numbers for pages.", "error")
            return redirect(url_for("book.edit_book", title=title))

        # Status logic
        if new_status == "completed":
            pages_to_add = book.total_pages - book.pages_read
            if pages_to_add > 0:
                book.reading_sessions.append({"pages": pages_to_add, "date": str(date.today())})
            book.pages_read = book.total_pages
            book.current_page = book.total_pages

        elif new_status == "to-read":
            book.pages_read = 0
            book.current_page = 0
            book.reading_sessions = []

        elif new_status == "reading":
            if book.status == "completed":
                book.pages_read = new_current_page
                book.reading_sessions = []
                if new_current_page > 0:
                    book.reading_sessions.append({"pages": new_current_page, "date": str(date.today())})
            else:
                pages_to_add = new_current_page - book.pages_read
                if pages_to_add > 0:
                    book.reading_sessions.append({"pages": pages_to_add, "date": str(date.today())})
                book.pages_read = max(book.pages_read, new_current_page)

            book.current_page = new_current_page

        book.status = new_status
        book.title = request.form["title"]
        book.author = request.form["author"]
        book.total_pages = total_pages

        reader.save_reader()
        flash("Book updated successfully!", "success")
        return redirect(url_for("library.library"))

    return render_template("library/index.html", books=reader.books, edit_book=book)


@book_bp.route('/delete-book/<string:title>')
@login_required
def delete_book(title):
    reader = load_reader()
    reader.books = [b for b in reader.books if b.title != title]
    reader.save_reader()
    flash(f"Book '{title}' deleted.", "info")
    return redirect(url_for('library.library'))


@book_bp.route('/book/<string:title>', methods=['GET', 'POST'])
@login_required
def book_detail(title):
    reader = load_reader()
    book = reader.find_book(title)

    if not book:
        flash("Book not found.", "error")
        return redirect(url_for('library.library'))

    today_str = date.today().isoformat()
    pages_today = sum(
    session["pages"]
    for session in book.reading_sessions
    if session["date"] == today_str
)

    dates = { session["date"] for session in book.reading_sessions }
    days_reading = len(dates)

    if request.method == 'POST':
        note_text = request.form.get('note')
        quote_text = request.form.get('quote')
        pages_str = request.form.get('pages_read')

        if note_text:
            book.add_note(note_text)
            flash("Note added successfully!", "success")

        if quote_text:
            book.add_quote(quote_text)
            flash("Quote added successfully!", "success")

        if pages_str:
            try:
                pages = int(pages_str)
                if pages <= 0:
                    flash("Pages must be greater than zero.", "error")
                    return redirect(url_for("book.book_detail", title=title))
                if book.pages_read + pages > book.total_pages:
                    flash(f"You cannot exceed the total pages ({book.total_pages}).", "error")
                    return redirect(url_for("book.book_detail", title=title))
                book.add_pages(pages)
                reader.log_reading(title, pages)
                flash(f"Progress updated: {book.pages_read}/{book.total_pages}", "success")
            except ValueError:
                flash("Invalid page number", "error")


        reader.save_reader()
        return redirect(url_for("book.book_detail", title=title))

    analytics = Analytics(reader)
    return render_template('book_detail.html', book=book, analytics=analytics,pages_today=pages_today,        days_reading=days_reading,    sessions=book.reading_sessions

)
