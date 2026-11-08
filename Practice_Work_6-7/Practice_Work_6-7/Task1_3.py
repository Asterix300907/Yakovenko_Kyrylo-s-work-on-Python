"""Cookies та sessions у Flask."""

from flask import Flask, request, make_response, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = "super-secret-key-for-session"  # для підпису сесій
app.json.ensure_ascii = False

# --- Робота з Cookies ---

@app.route("/set-theme/<theme>")
def set_theme(theme):
    """Встановити тему через cookie."""
    if theme not in ['light', 'dark', 'auto']:
        return jsonify({"error": "Недопустима тема. Дозволено: light, dark, auto"}), 400
    
    response = make_response(jsonify({"message": f"Тему '{theme}' встановлено"}))
    response.set_cookie(
        'theme', 
        theme, 
        max_age=30*24*60*60,  # 30 днів у секундах
        httponly=False,
        samesite='Lax'
    )
    return response


@app.route("/get-theme")
def get_theme():
    """Прочитати тему з cookie."""
    theme = request.cookies.get('theme', 'light')
    return jsonify({"theme": theme})


@app.route("/set-language/<lang>")
def set_language(lang):
    """Встановити мову через cookie."""
    if lang not in ['uk', 'en', 'ru']:
        return jsonify({"error": "Недопустима мова. Дозволено: uk, en, ru"}), 400
    
    response = make_response(jsonify({"message": f"Мову '{lang}' встановлено"}))
    response.set_cookie(
        'language', 
        lang, 
        max_age=365*24*60*60,  # 1 рік
        httponly=False,
        samesite='Lax'
    )
    return response


@app.route("/preferences")
def preferences():
    """Показати всі збережені уподобання з cookies."""
    prefs = {
        "theme": request.cookies.get('theme', 'light'),
        "language": request.cookies.get('language', 'uk')
    }
    return jsonify(prefs)


# --- Робота з Sessions ---

@app.route("/cart/add/<int:product_id>", methods=["GET", "POST"])
def add_to_cart(product_id):
    """Додати товар до кошика (session)."""
    if product_id not in products_db:
        return jsonify({"error": "Товар не знайдено"}), 404
    
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(product_id)
    session.modified = True  # важливо для збереження змін у списку
    
    product = products_db[product_id]
    return jsonify({
        "message": f"Товар '{product['name']}' додано до кошика",
        "cart": session['cart']
    })


@app.route("/cart")
def view_cart():
    """Переглянути кошик."""
    cart_ids = session.get('cart', [])
    
    items = []
    total = 0
    for pid in cart_ids:
        if pid in products_db:
            product = products_db[pid]
            items.append(product)
            total += product['price']
    
    return jsonify({
        "items": items,
        "total": total,
        "count": len(items)
    })


@app.route("/cart/clear", methods=["GET", "POST"])
def clear_cart():
    """Очистити кошик."""
    session.pop('cart', None)
    return jsonify({"message": "Кошик очищено"})


@app.route("/login", methods=["POST"])
def login():
    """Імітація входу — зберегти ім'я у session."""
    data = request.get_json(silent=True)
    if not data or 'username' not in data:
        return jsonify({"error": "Потрібен username"}), 400
    
    username = data['username']
    session['username'] = username
    
    return jsonify({"message": f"Вітаємо, {username}!"})


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Вихід — очистити session."""
    session.pop('username', None)
    return jsonify({"message": "Ви вийшли з системи"})


@app.route("/profile")
def profile():
    """Профіль користувача — залежить від session."""
    username = session.get('username')
    
    if not username:
        return jsonify({"error": "Ви не авторизовані"}), 401
    
    return jsonify({
        "username": username,
        "message": f"Це профіль користувача {username}"
    })


# Тимчасова "база" товарів
products_db = {
    1: {"name": "Ноутбук", "price": 25000},
    2: {"name": "Смартфон", "price": 12000},
    3: {"name": "Навушники", "price": 2000},
}


if __name__ == "__main__":
    app.run(debug=True, port=5000)