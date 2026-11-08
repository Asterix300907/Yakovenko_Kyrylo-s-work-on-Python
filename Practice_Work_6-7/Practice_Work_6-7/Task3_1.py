"""REST API для ресурсу 'Студент'."""

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.json.ensure_ascii = False 

# "База даних" студентів
students_db = {}
next_id = 1


# --- REST API ендпоінти ---


@app.route("/api/students", methods=["GET"])
def get_students():
    """GET /api/students — список усіх студентів з фільтрацією, сортуванням та пагінацією."""
    # Отримуємо параметри фільтрації
    group = request.args.get('group')
    min_gpa = request.args.get('min_gpa', type=float)
    
    # Параметри сортування
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    
    # Параметри пагінації
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Валідація пагінації
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10
    
    # Фільтруємо
    filtered = list(students_db.values())
    
    if group:
        filtered = [s for s in filtered if s['group'] == group]
    
    if min_gpa is not None:
        filtered = [s for s in filtered if s['gpa'] >= min_gpa]
    
    # Сортуємо
    if sort_by in ['name', 'gpa', 'group']:
        reverse = (order == 'desc')
        filtered.sort(key=lambda x: x[sort_by], reverse=reverse)
    
    # Пагінація
    total = len(filtered)
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    
    if page > total_pages:
        page = total_pages if total_pages > 0 else 1
    
    start = (page - 1) * per_page
    end = start + per_page
    page_students = filtered[start:end]
    
    return jsonify({
        "count": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "students": page_students
    }), 200


@app.route("/api/students", methods=["POST"])
def create_student():
    """POST /api/students — створити студента."""
    global next_id
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Очікується JSON тіло запиту", "status": 400}), 400
    
    # Валідація обов'язкових полів
    name = data.get('name', '').strip() if data.get('name') else ''
    group = data.get('group', '').strip() if data.get('group') else ''
    email = data.get('email', '').strip() if data.get('email') else ''
    gpa = data.get('gpa')
    
    if not name:
        return jsonify({"error": "Поле 'name' є обов'язковим", "status": 422}), 422
    if not group:
        return jsonify({"error": "Поле 'group' є обов'язковим", "status": 422}), 422
    
    # Валідація GPA
    if gpa is None:
        return jsonify({"error": "Поле 'gpa' є обов'язковим", "status": 422}), 422
    try:
        gpa = float(gpa)
    except (TypeError, ValueError):
        return jsonify({"error": "Поле 'gpa' має бути числом", "status": 422}), 422
    
    if gpa < 0 or gpa > 100:
        return jsonify({"error": "Поле 'gpa' має бути в діапазоні 0-100", "status": 422}), 422
    
    # Перевірка унікальності email
    if email:
        for s in students_db.values():
            if s['email'].lower() == email.lower():
                return jsonify({"error": f"Email '{email}' вже використовується", "status": 422}), 422
    
    # Створюємо студента
    new_student = {
        "id": next_id,
        "name": name,
        "group": group,
        "email": email,
        "gpa": gpa,
        "created_at": datetime.now().isoformat()
    }
    
    students_db[next_id] = new_student
    next_id += 1
    
    return jsonify(new_student), 201


@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """GET /api/students/:id — отримати конкретного студента."""
    student = students_db.get(student_id)
    if not student:
        return jsonify({"error": "Студента не знайдено", "status": 404}), 404
    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """PUT /api/students/:id — повне оновлення студента."""
    student = students_db.get(student_id)
    if not student:
        return jsonify({"error": "Студента не знайдено", "status": 404}), 404
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Очікується JSON тіло запиту", "status": 400}), 400
    
    # PUT — повне оновлення, всі поля обов'язкові
    name = data.get('name', '').strip() if data.get('name') else ''
    group = data.get('group', '').strip() if data.get('group') else ''
    email = data.get('email', '').strip() if data.get('email') else ''
    gpa = data.get('gpa')
    
    if not name:
        return jsonify({"error": "Поле 'name' є обов'язковим", "status": 422}), 422
    if not group:
        return jsonify({"error": "Поле 'group' є обов'язковим", "status": 422}), 422
    if gpa is None:
        return jsonify({"error": "Поле 'gpa' є обов'язковим", "status": 422}), 422
    
    try:
        gpa = float(gpa)
    except (TypeError, ValueError):
        return jsonify({"error": "Поле 'gpa' має бути числом", "status": 422}), 422
    
    if gpa < 0 or gpa > 100:
        return jsonify({"error": "Поле 'gpa' має бути в діапазоні 0-100", "status": 422}), 422
    
    # Перевірка унікальності email (крім поточного студента)
    if email:
        for sid, s in students_db.items():
            if sid != student_id and s['email'].lower() == email.lower():
                return jsonify({"error": f"Email '{email}' вже використовується", "status": 422}), 422
    
    # Оновлюємо всі поля
    student['name'] = name
    student['group'] = group
    student['email'] = email
    student['gpa'] = gpa
    student['updated_at'] = datetime.now().isoformat()
    
    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["PATCH"])
def patch_student(student_id):
    """PATCH /api/students/:id — часткове оновлення студента."""
    student = students_db.get(student_id)
    if not student:
        return jsonify({"error": "Студента не знайдено", "status": 404}), 404
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Очікується JSON тіло запиту", "status": 400}), 400
    
    # Оновлюємо тільки передані поля
    if 'name' in data:
        name = data['name'].strip() if data['name'] else ''
        if not name:
            return jsonify({"error": "Поле 'name' не може бути порожнім", "status": 422}), 422
        student['name'] = name
    
    if 'group' in data:
        group = data['group'].strip() if data['group'] else ''
        if not group:
            return jsonify({"error": "Поле 'group' не може бути порожнім", "status": 422}), 422
        student['group'] = group
    
    if 'email' in data:
        email = data['email'].strip() if data['email'] else ''
        # Перевірка унікальності
        if email:
            for sid, s in students_db.items():
                if sid != student_id and s['email'].lower() == email.lower():
                    return jsonify({"error": f"Email '{email}' вже використовується", "status": 422}), 422
        student['email'] = email
    
    if 'gpa' in data:
        gpa = data['gpa']
        try:
            gpa = float(gpa)
        except (TypeError, ValueError):
            return jsonify({"error": "Поле 'gpa' має бути числом", "status": 422}), 422
        if gpa < 0 or gpa > 100:
            return jsonify({"error": "Поле 'gpa' має бути в діапазоні 0-100", "status": 422}), 422
        student['gpa'] = gpa
    
    student['updated_at'] = datetime.now().isoformat()
    
    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """DELETE /api/students/:id — видалити студента."""
    student = students_db.get(student_id)
    if not student:
        return jsonify({"error": "Студента не знайдено", "status": 404}), 404
    
    del students_db[student_id]
    return '', 204


@app.route("/api/students/stats", methods=["GET"])
def students_stats():
    """GET /api/students/stats — статистика по студентах."""
    students = list(students_db.values())
    total = len(students)
    
    if total == 0:
        return jsonify({
            "total": 0,
            "avg_gpa": 0,
            "groups": {},
            "top_students": []
        }), 200
    
    # Середній GPA
    avg_gpa = round(sum(s['gpa'] for s in students) / total, 2)
    
    # Кількість студентів по групах
    groups = {}
    for s in students:
        group = s['group']
        groups[group] = groups.get(group, 0) + 1
    
    # Топ-3 студенти за GPA
    top_students = sorted(students, key=lambda x: x['gpa'], reverse=True)[:3]
    
    return jsonify({
        "total": total,
        "avg_gpa": avg_gpa,
        "groups": groups,
        "top_students": top_students
    }), 200


# --- Обробка помилок ---


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ресурс не знайдено", "status": 404}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Некоректний запит", "status": 400}), 400


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"error": "Помилка валідації", "status": 422}), 422


if __name__ == "__main__":
    # Заповнити тестовими даними
    test_students = [
        {"name": "Іваненко О.", "group": "КІ-21", "email": "ivan@kpi.ua", "gpa": 85.5},
        {"name": "Петренко М.", "group": "КІ-21", "email": "petro@kpi.ua", "gpa": 92.0},
        {"name": "Сидоренко А.", "group": "КІ-22", "email": "syd@kpi.ua", "gpa": 78.3},
        {"name": "Коваль Л.", "group": "КІ-22", "email": "koval@kpi.ua", "gpa": 95.1},
    ]
    for s in test_students:
        students_db[next_id] = {**s, "id": next_id,
                                 "created_at": datetime.now().isoformat()}
        next_id += 1

    app.run(debug=True, port=5000)