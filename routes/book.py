from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.helpers import load_reader
from utils.decorators import login_required
from models.book import Book
from models.analytics import Analytics
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

    if total_pages <= 0:
        flash("Total pages must be greater than 0.", "error")
        return redirect(url_for("library.library"))

    if current_page < 0 or current_page > total_pages:
        flash("Current page must be between 0 and total pages.", "error")
        return redirect(url_for("library.library"))

    new_book = Book(title=title, author=author, total_pages=total_pages, cover=cover_url, status=status)

    if status == "reading":
        new_book.set_current_page(current_page, reader)
    elif status == "completed":
        new_book.set_current_page(total_pages, reader)

    reader.add_book(new_book)
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

        if total_pages <= 0:
            flash("Total pages must be greater than 0.", "error")
            return redirect(url_for("book.edit_book", title=title))

        if new_current_page < 0 or new_current_page > total_pages:
            flash("Current page must be between 0 and total pages.", "error")
            return redirect(url_for("book.edit_book", title=title))

        book.title = request.form["title"]
        book.author = request.form["author"]
        book.total_pages = total_pages
        book.status = new_status

        if new_status == "completed":
            pages_to_add = book.total_pages - book.pages_read
            if pages_to_add > 0:
                today_str = str(date.today())
                for session in book.reading_sessions:
                    if session["date"] == today_str:
                        session["pages"] += pages_to_add
                        break
                else:
                    book.reading_sessions.append({"pages": pages_to_add, "date": today_str})

            book.pages_read = book.total_pages
            book.current_page = book.total_pages


        else:
            book.set_current_page(new_current_page, reader)

        reader.save_reader()
        flash("Book updated successfully!", "success")
        return redirect(url_for("library.library"))

    return render_template(
        "library/index.html",
        books=reader.books,
        edit_book=book
    )


@book_bp.route('/delete-book/<string:title>')
@login_required
def delete_book(title):
    reader = load_reader()
    reader.delete_book(title)
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

    if request.method == 'POST':
        pages_str = request.form.get('pages_read')
        if pages_str:
            try:
                new_current_page = int(pages_str)
                if new_current_page < 0:
                    flash("Current page cannot be negative.", "error")
                elif new_current_page > book.total_pages:
                    flash(f"Cannot exceed total pages ({book.total_pages}).", "error")
                else:
                    book.set_current_page(new_current_page, reader)
                    reader.save_reader()
                    flash(f"Progress updated: {book.pages_read}/{book.total_pages}", "success")
            except ValueError:
                flash("Invalid page number", "error")
        return redirect(url_for("book.book_detail", title=title))

    today_str = date.today().isoformat()
    pages_today = sum(
        session["pages"]
        for session in book.reading_sessions
        if session["date"] == today_str
    )
    days_reading = len({session["date"] for session in book.reading_sessions})
    analytics = Analytics(reader)

    return render_template(
        'book_detail.html',
        book=book,
        analytics=analytics,
        pages_today=pages_today,
        days_reading=days_reading,
        sessions=book.reading_sessions
    )
