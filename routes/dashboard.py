from flask import Blueprint, redirect, render_template, flash, url_for
from utils.decorators import login_required
from utils.helpers import load_reader
from models.analytics import Analytics

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    reader = load_reader()
    if not reader:
        flash("Please log in first.", "error")
        return redirect(url_for("auth.sign_in"))
    analytics = Analytics(reader)
    return render_template('dashboard.html', books=reader.books, analytics=analytics)
