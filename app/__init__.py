from flask import Flask
from flask_login import LoginManager
from app.blueprints import register_blueprints

from config import settings
from db.database import init_db, session_scope
from db.models import User
from utils.book_loader import add_books_to_db


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    with session_scope() as session:
        user = session.query(User).get(int(user_id))
        if user:
            session.expunge(user)
        return user


def create_app():
    init_db()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    add_books_to_db()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    register_blueprints(app)
    return app
