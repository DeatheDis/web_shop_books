import json
from db.database import session_scope
from db.models import Book
from config import settings
from utils.category_utils import get_category_by_genre


def add_books_to_db():
    try:
        with open(settings.BOOKS_DATABASE_PATH, 'r', encoding='utf-8') as f:
            books = json.load(f)
    except FileNotFoundError:
        print(f'Файл{settings.BOOKS_DATABASE_PATH} не найден')
        return
    except json.decoder.JSONDecodeError as e:
        print(f'Ошибка{e}')
        return

    with session_scope() as session:
        for data in books:
            existing_book = session.query(Book).filter_by(
                title=data.get('title', 'Неизвестно'),
                author=data.get('author', 'Неизвестно')
            ).first()

            if not existing_book:
                category = get_category_by_genre(data.get('genre', ''))
                book = Book(
                    title=data.get('title', 'Неизвестно'),
                    author=data.get('author', 'Неизвестно'),
                    year=data.get('year', 0),
                    price=data.get('price', 0.0),
                    genre=data.get('genre', 'Неизвестно'),
                    category=category,
                    cover=data.get('cover', ''),
                    description=data.get('description', ''),
                    rating=data.get('rating', 0.0),
                    reviews_count=data.get('reviews_count', 0),
                    binding_type=data.get('binding_type', 'Неизвестно'),
                    publisher=data.get('publisher', 'Неизвестно'),
                    age_limit=data.get('age_limit', 0),
                    weight=data.get('weight', 0.0),
                    format=data.get('format', 'Неизвестно')
                )
                session.add(book)

    print(f'Книги были импортированы в базу данных')

