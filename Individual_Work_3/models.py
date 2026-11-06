from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Book(db.Model):
    """Модель книги."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    isbn = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Зв'язок з замовленнями
    order_items = db.relationship('OrderItem', backref='book', lazy=True)
    
    def __repr__(self):
        return f'<Book {self.title}>'
    
    def to_dict(self):
        """Серіалізація для REST API."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'price': self.price,
            'stock': self.stock,
            'isbn': self.isbn,
            'created_at': self.created_at.isoformat()
        }


class Order(db.Model):
    """Модель замовлення."""
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')
    
    # Зв'язок з елементами замовлення
    items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def __repr__(self):
        return f'<Order {self.id}>'
    
    def total_price(self):
        """Обчислити загальну суму замовлення."""
        return sum(item.quantity * item.book.price for item in self.items)


class OrderItem(db.Model):
    """Елемент замовлення (зв'язок many-to-one з Order та Book)."""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'