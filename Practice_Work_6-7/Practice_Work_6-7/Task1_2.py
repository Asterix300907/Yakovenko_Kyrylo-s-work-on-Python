"""Views/контролери для обробки запитів у Flask."""

from flask import Flask, request, jsonify, abort, render_template_string
from functools import wraps

app = Flask(__name__)
app.json.ensure_ascii = False

def validate_json(required_fields):
    """Декоратор для валідації JSON-запитів."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            if data is None:
                return jsonify({"error": "Очікується JSON"}), 400
            missing = [field for field in required_fields if field not in data]
            if missing:
                return jsonify({
                    "error": f"Відсутні поля: {', '.join(missing)}"
                }), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator


# --- View-функції ---


@app.route("/api/items", methods=["GET"])
def get_items():
    """GET /api/items — список елементів з фільтрацією.

    Параметри запиту:
        category (str): фільтр за категорією
        min_price (float): мінімальна ціна
        max_price (float): максимальна ціна
        sort (str): поле сортування (name, price)
        order (str): напрямок (asc, desc)
    """
    # Зчитуємо параметри фільтрації
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_field = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc')

    # Фільтруємо елементи
    filtered_items = list(items_db.values())

    if category:
        filtered_items = [item for item in filtered_items 
                         if item['category'] == category]

    if min_price is not None:
        filtered_items = [item for item in filtered_items 
                         if item['price'] >= min_price]

    if max_price is not None:
        filtered_items = [item for item in filtered_items 
                         if item['price'] <= max_price]

    # Сортуємо
    reverse = (order == 'desc')
    if sort_field in ['name', 'price']:
        filtered_items.sort(key=lambda x: x[sort_field], reverse=reverse)

    # Повертаємо JSON зі списком та метаданими
    return jsonify({
        "items": filtered_items,
        "total": len(filtered_items),
        "filters": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price
        },
        "sort": {
            "field": sort_field,
            "order": order
        }
    }), 200


@app.route("/api/items", methods=["POST"])
@validate_json(["name", "price", "category"])
def create_item():
    """POST /api/items — створити елемент з валідацією."""
    global next_id
    
    # Зчитуємо JSON
    data = request.get_json()
    
    # Додаткова валідація
    if not data['name'] or not isinstance(data['name'], str):
        return jsonify({"error": "name має бути непорожнім рядком"}), 400
    
    if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
        return jsonify({"error": "price має бути додатним числом"}), 400
    
    if not isinstance(data['category'], str):
        return jsonify({"error": "category має бути рядком"}), 400
    
    # Створюємо новий елемент
    new_item = {
        "id": next_id,
        "name": data['name'],
        "price": data['price'],
        "category": data['category']
    }
    
    items_db[next_id] = new_item
    next_id += 1
    
    # Повертаємо 201 Created
    return jsonify(new_item), 201


@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """GET /api/items/:id — отримати деталі елемента."""
    item = items_db.get(item_id)
    
    if not item:
        abort(404)
    
    return jsonify(item), 200


@app.route("/api/items/<int:item_id>", methods=["PUT"])
@validate_json(["name", "price", "category"])
def update_item(item_id):
    """PUT /api/items/:id — оновити елемент повністю."""
    item = items_db.get(item_id)
    
    if not item:
        abort(404)
    
    # Зчитуємо JSON
    data = request.get_json()
    
    # Додаткова валідація
    if not data['name'] or not isinstance(data['name'], str):
        return jsonify({"error": "name має бути непорожнім рядком"}), 400
    
    if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
        return jsonify({"error": "price має бути додатним числом"}), 400
    
    if not isinstance(data['category'], str):
        return jsonify({"error": "category має бути рядком"}), 400
    
    # Оновлюємо елемент
    item['name'] = data['name']
    item['price'] = data['price']
    item['category'] = data['category']
    
    return jsonify(item), 200


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """DELETE /api/items/:id — видалити елемент."""
    item = items_db.get(item_id)
    
    if not item:
        abort(404)
    
    # Видаляємо елемент
    del items_db[item_id]
    
    # Повертаємо 204 No Content
    return '', 204


# --- Обробка помилок ---


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ресурс не знайдено"}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Некоректний запит"}), 400


# Тимчасова "база даних"
items_db = {
    1: {"id": 1, "name": "Ноутбук", "price": 25000, "category": "електроніка"},
    2: {"id": 2, "name": "Книга Python", "price": 500, "category": "книги"},
    3: {"id": 3, "name": "Навушники", "price": 2000, "category": "електроніка"},
}
next_id = 4


if __name__ == "__main__":
    app.run(debug=True, port=5000)