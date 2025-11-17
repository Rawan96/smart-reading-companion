from flask import session
from models.reader import Reader

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def get_current_user_email():
    return session.get("user")

def load_reader():
    email = get_current_user_email()
    if email:
        return Reader.load_reader(email)
    return None

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
