from datetime import datetime

from flask_login import UserMixin

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=32))
    surname: str = Column(String(length=32))
    email: str = Column(String(length=120), unique=True)
    phone: str = Column(String(length=20), unique=True)
    password_hash: str = Column(String(length=256))

    reviews = relationship('Review', back_populates='user', cascade='all, delete-orphan')
    cart_items = relationship('CartItem', back_populates='user', cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')


class Book(Base):
    __tablename__ = 'books'
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(length=100))
    author: str = Column(String(length=100))
    year: int = Column(Integer)
    price: float = Column(Float)
    genre: str = Column(String(length=100))
    category: str = Column(String(length=100))
    cover: str = Column(String())
    description: str = Column(String(length=300))
    rating: float = Column(Float, default=0.0)
    reviews_count: int = Column(Integer, default=0)
    binding_type: str = Column(String(50))
    publisher: str = Column(String(length=100))
    age_limit: int = Column(Integer)
    weight: float = Column(Float)
    format: str = Column(String(length=50))

    reviews = relationship('Review', back_populates='book', cascade='all, delete-orphan')
    cart_items = relationship('CartItem', back_populates='book', cascade='all, delete-orphan')
    order_items = relationship('OrderItem', back_populates='book', cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_items'
    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    book_id: int = Column(Integer, ForeignKey('books.id'))
    count: int = Column(Integer)

    user = relationship('User', back_populates='cart_items')
    book = relationship('Book', back_populates='cart_items')


class Order(Base):
    __tablename__ = 'orders'
    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    date: datetime = Column(DateTime)
    status: str = Column(String(length=80))
    address: str = Column(String(length=80))
    delivery_date = Column(Date, nullable=True)

    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')


class OrderItem(Base):
    __tablename__ = 'order_items'
    id: int = Column(Integer, primary_key=True)
    book_id: int = Column(Integer, ForeignKey('books.id'))
    order_id: int = Column(Integer, ForeignKey('orders.id'))
    count: int = Column(Integer)
    price: float = Column(Float)

    order = relationship('Order', back_populates='items')
    book = relationship('Book', back_populates='order_items')


class Review(Base):
    __tablename__ = 'reviews'
    id: int = Column(Integer, primary_key=True)
    review: str = Column(Text)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    book_id: int = Column(Integer, ForeignKey('books.id'))
    grade: int = Column(Integer)

    user = relationship('User', back_populates='reviews')
    book = relationship('Book', back_populates='reviews')
