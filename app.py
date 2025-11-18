import os
from flask import Flask,redirect, url_for,session


app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
app.config["UPLOAD_FOLDER"] = os.path.join("static", "book_covers")



@app.route('/')
def home():
    if "user" in session:
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("auth.sign_up"))


from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.library import library_bp
from routes.book import book_bp
from routes.search import search_bp
from routes.goals import goals_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp,)
app.register_blueprint(library_bp)
app.register_blueprint(book_bp)
app.register_blueprint(search_bp)
app.register_blueprint(goals_bp)


if __name__ == '__main__':
    app.run(debug=True)
