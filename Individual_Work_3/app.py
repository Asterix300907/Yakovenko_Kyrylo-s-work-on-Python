from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from models import db, Book, Order, OrderItem
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Контекстний процесор — додає cart_total до всіх шаблонів
@app.context_processor
def cart_count():
    """Додати загальну кількість книг у кошику до всіх шаблонів."""
    cart = session.get('cart', {})
    total_items = sum(cart.values()) if isinstance(cart, dict) else len(cart) if isinstance(cart, list) else 0
    return {'cart_total': total_items}


# Створення таблиць при першому запуску
with app.app_context():
    db.create_all()
    # Додати тестові книги, якщо база порожня
    if Book.query.count() == 0:
        test_books = [
            Book(title='Python для початківців', author='Іван Петренко', genre='Програмування', price=450, stock=10, isbn='978-1234567890'),
            Book(title='Django в дії', author='Марія Сидоренко', genre='Програмування', price=650, stock=5, isbn='978-1234567891'),
            Book(title='Flask розробка', author='Олексій Коваль', genre='Програмування', price=550, stock=8, isbn='978-1234567892'),
            Book(title='Алгоритми та структури даних', author='Петро Шевченко', genre='Комп\'ютерні науки', price=750, stock=3, isbn='978-1234567893'),
            Book(title='Машинне навчання', author='Анна Бондар', genre='Data Science', price=850, stock=7, isbn='978-1234567894'),
        ]
        db.session.add_all(test_books)
        db.session.commit()


# ============================================================
# ВЕБ-МАРШРУТИ
# ============================================================

@app.route('/')
def index():
    """Головна сторінка."""
    books = Book.query.all()
    theme = request.cookies.get('theme', 'light')
    return render_template('index.html', books=books, theme=theme)


@app.route('/books')
def book_list():
    """Список книг з фільтрацією."""
    genre = request.args.get('genre')
    if genre:
        books = Book.query.filter_by(genre=genre).all()
    else:
        books = Book.query.all()
    return render_template('books.html', books=books)


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    """Деталі книги."""
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/cart/add/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    """Додати книгу до кошика (збільшити кількість якщо вже є)."""
    book = Book.query.get_or_404(book_id)
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    # Якщо старий формат (список) — конвертуємо
    if isinstance(cart, list):
        cart = {str(bid): 1 for bid in cart}

    cart[str(book_id)] = cart.get(str(book_id), 0) + 1
    session['cart'] = cart
    session.modified = True

    flash(f'Книгу "{book.title}" додано до кошика!', 'success')
    return redirect(url_for('book_list'))


@app.route('/cart/update/<int:book_id>', methods=['POST'])
def update_cart(book_id):
    """Змінити кількість книги в кошику."""
    if 'cart' not in session:
        return redirect(url_for('view_cart'))

    action = request.form.get('action')  # 'increase', 'decrease', 'remove'
    cart = session['cart']

    # Конвертація старого формату
    if isinstance(cart, list):
        cart = {str(bid): 1 for bid in cart}

    book_id_str = str(book_id)
    if book_id_str not in cart:
        return redirect(url_for('view_cart'))

    if action == 'increase':
        cart[book_id_str] += 1
    elif action == 'decrease':
        cart[book_id_str] -= 1
        if cart[book_id_str] <= 0:
            del cart[book_id_str]
    elif action == 'remove':
        del cart[book_id_str]

    session['cart'] = cart
    session.modified = True

    if not cart:
        flash('Кошик порожній', 'info')
    return redirect(url_for('view_cart'))


@app.route('/cart')
def view_cart():
    """Переглянути кошик з кількістю."""
    cart = session.get('cart', {})

    # Конвертація старого формату (список → словник)
    if isinstance(cart, list):
        cart = {str(bid): 1 for bid in cart}
        session['cart'] = cart

    books_data = []
    total = 0

    for book_id_str, quantity in cart.items():
        book = Book.query.get(int(book_id_str))
        if book:
            books_data.append({
                'book': book,
                'quantity': quantity,
                'subtotal': book.price * quantity
            })
            total += book.price * quantity

    return render_template('cart.html', books_data=books_data, total=total)


@app.route('/cart/clear')
def clear_cart():
    """Очистити кошик."""
    session.pop('cart', None)
    flash('Кошик очищено', 'info')
    return redirect(url_for('view_cart'))


@app.route('/order', methods=['GET', 'POST'])
def create_order():
    """Оформити замовлення."""
    if request.method == 'POST':
        customer_name = request.form.get('name')
        customer_email = request.form.get('email')

        if not customer_name or not customer_email:
            flash('Заповніть всі поля!', 'error')
            return redirect(url_for('create_order'))

        cart = session.get('cart', {})
        if isinstance(cart, list):
            cart = {str(bid): 1 for bid in cart}

        if not cart:
            flash('Кошик порожній!', 'error')
            return redirect(url_for('view_cart'))

        # Створити замовлення
        order = Order(customer_name=customer_name, customer_email=customer_email)
        db.session.add(order)
        db.session.flush()  # Отримати ID замовлення

        # Додати елементи замовлення з кількістю
        for book_id_str, quantity in cart.items():
            item = OrderItem(order_id=order.id, book_id=int(book_id_str), quantity=quantity)
            db.session.add(item)

        db.session.commit()
        session.pop('cart', None)

        flash(f'Замовлення #{order.id} успішно оформлено!', 'success')
        return redirect(url_for('index'))

    return render_template('order.html')


@app.route('/set-theme/<theme>')
def set_theme(theme):
    """Встановити тему через cookie."""
    response = make_response(redirect(request.referrer or url_for('index')))
    response.set_cookie('theme', theme, max_age=30*24*60*60)
    return response


# ============================================================
# REST API
# ============================================================

@app.route('/api/books', methods=['GET'])
def api_get_books():
    """GET /api/books — список книг."""
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])


@app.route('/api/books/<int:book_id>', methods=['GET'])
def api_get_book(book_id):
    """GET /api/books/<id> — деталі книги."""
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())


@app.route('/api/books', methods=['POST'])
def api_create_book():
    """POST /api/books — створити книгу."""
    data = request.get_json()
    book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        price=data['price'],
        stock=data.get('stock', 0),
        isbn=data.get('isbn')
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def api_update_book(book_id):
    """PUT /api/books/<id> — оновити книгу."""
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre = data.get('genre', book.genre)
    book.price = data.get('price', book.price)
    book.stock = data.get('stock', book.stock)
    db.session.commit()
    return jsonify(book.to_dict())


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def api_delete_book(book_id):
    """DELETE /api/books/<id> — видалити книгу."""
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)