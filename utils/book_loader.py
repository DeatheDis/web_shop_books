import json
from db.database import session_scope
from db.models import Book


json_path = r'D:\Backend\web_shop_books\data\books_catalog.json'


def add_books_to_db():
    with open(json_path, 'r', encoding='utf-8') as f:
        books = json.load(f)
        with session_scope() as session:
            for data in books:
                book = Book(title=data['title'],
                            author=data['author'],
                            year=data['year'],
                            price=data['price'],
                            genre=data['genre'],
                            cover=data['cover'],
                            description=data['description'],
                            rating=data['rating'])
                session.add(book)

        print(f'Книги были импортированы в базу данных')

