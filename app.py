from flask import Flask, render_template,request, redirect, url_for, flash
from models.book import Book
from models.reader import Reader
from models.analytics import Analytics

app = Flask(__name__)

reader = Reader('Rawan')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/library')
def library():
    return render_template("library.html", books = reader.books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get("title")
    author = request.form.get("author")
    total_pages = int(request.form.get('total_pages', 0))
    genre = request.form.get("genre")

    if title and author and total_pages > 0:
        new_book = Book(title, author, total_pages, genre)
        reader.add_book(new_book)
    return redirect(url_for('library'))


@app.route('/update_progress/<string:title>', methods=['POST'])
def update_progress(title):
    pages = int(request.form.get('pages'))
    if pages <= 0:
        return redirect(url_for('library'))

    book = next((b for b in reader.books if b.title == title),None)

    if not book:
        flash('Book not found.',"error")
        return redirect(url_for('library'))
    remaining_pages =book.total_pages - book.pages_read

    if pages > remaining_pages:
        flash(f"You only have {remaining_pages} pages left in '{book.title}'.", "error")
        return redirect(url_for('library'))
    reader.log_reading(title, pages)

    if book.pages_read >= book.total_pages:
        flash(f"Congratulations! You’ve completed '{book.title}'", "success")

    return redirect(url_for('library'))


@app.route('/delete-book/<string:title>')
def delete_book(title):
    reader.remove_book(title)
    return redirect(url_for('library'))


@app.route('/book/<string:title>', methods=['GET', 'POST'])
def book_detail(title):
    book = next((b for b in reader.books if b.title == title), None)
    if not book:
        return redirect(url_for('library'))

    if request.method == 'POST':
        note_text = request.form.get('note')
        if note_text:
            book.add_note(note_text)
        return redirect(url_for('book_detail', title=title))

    book_analytics = Analytics(reader)
    return render_template(
        'book_detail.html',
        book=book,
        analytics=book_analytics
    )


if __name__ == '__main__':
    app.run(debug=True)
