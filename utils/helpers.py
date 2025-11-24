from flask import session
from models.reader import Reader

def get_current_user_email():
    return session.get("user")

def load_reader():
    email = get_current_user_email()
    if email:
        return Reader.load_reader(email)
    return None

