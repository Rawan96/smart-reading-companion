from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_book')
def add_book():
    return render_template('add_book.html')




if __name__ == '__main__':
    app.run(debug=True)
