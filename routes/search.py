from flask import Blueprint, render_template, request, url_for
from utils.helpers import load_reader

search_bp = Blueprint('search', __name__)


@search_bp.route("/search")
def search():
    reader = load_reader()
    query = request.args.get("q", "").lower()
    books = reader.books

    if query:
        books = [b for b in books if query in b.title.lower() or query in b.author.lower()]

    view = request.args.get("view", "list")  # list or grid

    if view == "grid":
        template = "library/_search_results_grid.html"
    else:
        template = "library/_search_results_list.html"

    return render_template(template, books=books)
