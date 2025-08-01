from flask import render_template, abort, flash, redirect, request, url_for
from flask_login import login_required, current_user
from db.models import Book, Review
from db.database import session_scope
from sqlalchemy.orm import joinedload
from app.forms import ReviewForm
from . import book_blueprint


@book_blueprint.route('/book/<int:book_id>/', methods=['GET'])
def book(book_id):
    with session_scope() as session:
        book = session.query(Book).options(
            joinedload(Book.reviews).joinedload(Review.user)
        ).get(book_id)
        if not book:
            abort(404)

        form = ReviewForm()
        return render_template('book_info.html', book=book, form=form)


@book_blueprint.route('/book/<int:book_id>/add_review', methods=['POST'])
@login_required
def add_review(book_id):
    form = ReviewForm()
    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form, field).label.text}: {error}', 'danger')
        return redirect(url_for('book.book', book_id=book_id))

    with session_scope() as session:
        book = session.query(Book).options(
            joinedload(Book.reviews).joinedload(Review.user)
        ).get(book_id)
        if not book:
            abort(404)

        new_review = Review(
            review=form.review.data,
            grade=int(form.grade.data),
            user_id=current_user.id,
            book_id=book_id
        )
        session.add(new_review)
        session.flush()

        all_grades = [r.grade for r in book.reviews] + [int(form.grade.data)]
        book.reviews_count = len(all_grades)
        book.rating = sum(all_grades) / len(all_grades)

        flash('Спасибо за ваш отзыв!', 'success')

    return redirect(url_for('book.book', book_id=book_id))


