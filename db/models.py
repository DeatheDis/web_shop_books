from datetime import datetime

from flask_login import UserMixin

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=32))
    surname: str = Column(String(length=32))
    email: str = Column(String(length=120), unique=True)
    phone: str = Column(String(length=20), unique=True)
    password_hash: str = Column(String(length=256))


class Book(Base):
    __tablename__ = 'books'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=80))
    author: str = Column(String(length=80))
    price: float = Column(Float)
    genre: str = Column(String(length=80))
    cover: str = Column(String(length=80))
    description: str = Column(String(length=300))
    rating: int = Column(Integer)


class CartItem(Base):
    __tablename__ = 'cart_items'
    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    book_id: int = Column(Integer, ForeignKey('books.id'))
    count: int = Column(Integer)


class Order(Base):
    __tablename__ = 'orders'
    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    date: datetime = Column(DateTime)
    status: str = Column(String(length=80))
    address: str = Column(String(length=80))
    books_list: list = Column(String(length=80))


class OrderItem(Base):
    __tablename__ = 'order_items'
    id: int = Column(Integer, primary_key=True)
    book_id: int = Column(Integer, ForeignKey('books.id'))
    count: int = Column(Integer)
    price: float = Column(Float)


class Review(Base):
    __tablename__ = 'reviews'
    id: int = Column(Integer, primary_key=True)
    review: str = Column(String(length=80))
    user_id: int = Column(Integer, ForeignKey('users.id'))
    book_id: int = Column(Integer, ForeignKey('books.id'))
    grade: int = Column(Integer)






