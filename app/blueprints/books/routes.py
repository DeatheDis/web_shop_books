from flask import render_template, redirect, url_for, flash, request, abort
from db.models import User, Book
from db.database import session_scope
from . import book_blueprint


@book_blueprint.route('/book/<int:book_id>/', methods=['GET'])
def book(book_id):
    with session_scope() as session:
        book = session.query(Book).get(book_id)
        if not book:
            abort(404)

        return render_template('book_info.html', book=book)
