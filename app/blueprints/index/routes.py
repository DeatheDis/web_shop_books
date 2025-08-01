from flask import render_template, redirect, url_for, flash, request
from db.database import session_scope
from db.models import Book

from utils.category_utils import PREDEFINED_CATEGORIES
from utils.category_utils import get_all_categories
from . import main_blueprint


@main_blueprint.app_context_processor
def inject_categories():
    with session_scope() as session:
        all_categories = get_all_categories(session)

    main_categories = list(all_categories.keys())
    return dict(main_categories=main_categories, all_categories=all_categories)


@main_blueprint.route('/')
def main():
    with session_scope() as session:
        top_books = session.query(Book).order_by(Book.rating.desc()).limit(3).all()
        categories = list(PREDEFINED_CATEGORIES.keys())
        return render_template('index.html', top_books=top_books, categories=categories)


@main_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    user_search = request.args.get('q', '').strip()
    if not user_search:
        flash('Введите поисковый запрос', 'info')
        return redirect(url_for('index.main'))

    with session_scope() as session:
        books = session.query(Book).filter(
            Book.title.ilike(f'%{user_search}%') |
            Book.author.ilike(f'%{user_search}%') |
            Book.genre.ilike(f'%{user_search}%')).all()

        return render_template('search.html', books=books, user_search=user_search)


@main_blueprint.route('/category/<category_name>')
@main_blueprint.route('/category/<category_name>/<genre>')
def books_by_category(category_name, genre=None):
    with session_scope() as session:
        all_categories = get_all_categories(session)

        all_known_genres = {g for genres in all_categories.values() for g in genres}

        books = []
        genres_in_category = []

        if category_name in all_categories:
            genres_in_category = all_categories[category_name]

            if genre:
                books = session.query(Book).filter(Book.genre == genre).all()
                selected_genre = genre
            else:
                books = session.query(Book).filter(Book.genre.in_(genres_in_category)).all()
                selected_genre = None

        elif category_name.lower() == 'все книги':
            books = session.query(Book).all()
            selected_genre = None

        elif category_name.lower() == 'другое':
            books = session.query(Book).filter(
                (Book.genre == None) | (~Book.genre.in_(all_known_genres))
            ).all()
            selected_genre = None

        else:
            selected_genre = None

    return render_template(
        'category.html',
        books=books,
        category=category_name,
        genres_in_category=genres_in_category,
        selected_genre=selected_genre,
        main_categories=list(all_categories.keys()),
        all_categories=all_categories
    )
