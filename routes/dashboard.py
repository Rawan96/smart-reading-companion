from datetime import datetime
from flask import Blueprint, redirect, render_template, flash, url_for,session
from utils.decorators import login_required
from utils.helpers import load_reader
from models.analytics import Analytics

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    email = session.get("user")
    reader = load_reader()
    analytics = Analytics(reader)

    if not reader:
        flash("User not found.", "error")
        session.pop("user", None)
        return redirect(url_for("auth.sign_in"))

    if not email:
        flash("Please log in first.", "error")
        return redirect(url_for("auth.sign_in"))


    if not reader:
        flash("User not found.", "error")
        return redirect(url_for("auth.sign_in"))


    #Chart data
    def get_books_per_month(books):
        month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        months = {m: 0 for m in month_order}

        for b in books:
            if b.reading_sessions:
                for session in b.reading_sessions:
                    date = datetime.strptime(session['date'], "%Y-%m-%d")
                    month_key = date.strftime("%b")
                    months[month_key] += 1

        labels = month_order
        data = [months[m] for m in labels]
        return labels, data

    def get_pages_per_month(books):
        month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        pages_per_month = {m: 0 for m in month_order}

        for b in books:
            for session in b.reading_sessions:
                date = datetime.strptime(session["date"], "%Y-%m-%d")
                month_key = date.strftime("%b")
                pages_per_month[month_key] += session["pages"]

        labels = month_order
        data = [pages_per_month[m] for m in labels]
        return labels, data

    books_labels, books_data = get_books_per_month(reader.books)
    pages_labels, pages_data = get_pages_per_month(reader.books)

    stats = {
        "total_books": analytics.total_books(),
        "total_pages_read": analytics.total_pages_read(),
        "completion_rate": analytics.completion_rate(),
        "average_books_monthly": analytics.average_books_monthly(),
        "books_labels": books_labels,
        "books_data": books_data,
        "pages_labels": pages_labels,
        "pages_data": pages_data,
    }

    return render_template(
        'dashboard.html',
        analytics=analytics,
        books=reader.books,
        stats=stats,
        name=reader.name
    )
