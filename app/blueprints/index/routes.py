from flask import render_template, redirect, url_for, flash, request
from app.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from db.database import session_scope
from db.models import User, Book

from . import main_blueprint


@main_blueprint.route('/')
def main():
    with session_scope() as session:
        top_books = session.query(Book).order_by(Book.rating.desc()).limit(3).all()
        return render_template('index.html', top_books=top_books)


@main_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    search = request.args.get('q', '')
    if search:
        return render_template('search.html', search=search)

    return render_template('index.html')


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(User).filter_by(email=form.email.data).first()
            if user:
                flash(message='User with this email already exists.', category='danger')
                return redirect(url_for('index.register'))
        user = User(name=form.name.data,
                    surname=form.surname.data,
                    email=form.email.data,
                    phone=form.phone_number.data,
                    password_hash=generate_password_hash(form.password.data))
        with session_scope() as session:
            session.add(user)
        return redirect(url_for('index.login'))
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "danger")

    return render_template('register.html', form=form)


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(User).filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user=user)
                return redirect(url_for('index.main'))
        flash('Login failed.', 'danger')
    return render_template('login.html', form=form)


@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.main'))

