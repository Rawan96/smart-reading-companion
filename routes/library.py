from flask import Blueprint, render_template, request
from utils.decorators import login_required
from utils.helpers import load_reader


library_bp = Blueprint('library', __name__)

@library_bp.route('/library')
@login_required
def library():
    reader = load_reader()
    search_query = request.args.get('q', '').lower()
    books = reader.books
    if search_query:
        books = [b for b in books if search_query in b.title.lower() or search_query in b.author.lower()]
    return render_template('library/index.html', books=books, query=search_query)
