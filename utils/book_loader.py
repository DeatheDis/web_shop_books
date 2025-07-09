import json
from db.database import session_scope
from db.models import Book


json_path = r'D:\Backend\web_shop_books\data\books_catalog.json'


def add_books_to_db():
    with open(json_path, 'r', encoding='utf-8') as f:
        books = json.load(f)

        with session_scope() as session:
            for data in books:
                book = Book(
                    title=data.get('title', 'Неизвестно'),
                    author=data.get('author', 'Неизвестно'),
                    year=data.get('year', 0),
                    price=data.get('price', 0.0),
                    genre=data.get('genre', 'Неизвестно'),
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

