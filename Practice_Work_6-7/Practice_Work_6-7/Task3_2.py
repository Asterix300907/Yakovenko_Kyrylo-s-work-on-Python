"""REST API: серіалізація, фільтрація, обробка помилок."""

from flask import Flask, request, jsonify, g
from datetime import datetime
from functools import wraps
import time

app = Flask(__name__)
app.json.ensure_ascii = False


# --- Серіалізатор ---


class StudentSerializer:
    """Серіалізатор для перетворення даних студента."""

    ALLOWED_FIELDS = {'id', 'name', 'group', 'email', 'gpa', 'created_at', 'updated_at'}

    @staticmethod
    def serialize(student: dict, fields: list[str] | None = None) -> dict:
        """Серіалізувати студента (вибрати потрібні поля)."""
        if fields:
            want_grade = 'grade' in fields
            effective_fields = set(fields)

            if want_grade and 'gpa' not in effective_fields:
                effective_fields.add('gpa')

            filtered = {
                k: v for k, v in student.items()
                if k in effective_fields and k in StudentSerializer.ALLOWED_FIELDS
            }
        else:
            filtered = {
                k: v for k, v in student.items()
                if k in StudentSerializer.ALLOWED_FIELDS
            }

        # Обчислюємо grade, якщо gpa є в результаті
        if 'gpa' in filtered:
            gpa = filtered['gpa']
            if gpa >= 90:
                filtered['grade'] = 'відмінно'
            elif gpa >= 75:
                filtered['grade'] = 'добре'
            elif gpa >= 60:
                filtered['grade'] = 'задовільно'
            else:
                filtered['grade'] = 'незадовільно'

        # Якщо користувач не запитував gpa, але ми додали його для обчислення — прибираємо
        if fields and 'gpa' not in fields and 'gpa' in filtered and 'grade' in filtered:
            del filtered['gpa']

        return filtered

    @staticmethod
    def deserialize(data: dict) -> tuple[dict | None, list[str]]:
        """Десеріалізувати вхідні дані з валідацією."""
        errors = []
        cleaned = {}

        if not data:
            return None, ["Очікується JSON тіло запиту"]

        name = data.get('name')
        if name is None:
            errors.append("Поле 'name' є обов'язковим")
        elif not isinstance(name, str) or not name.strip():
            errors.append("Поле 'name' має бути непорожнім рядком")
        else:
            cleaned['name'] = name.strip()

        group = data.get('group')
        if group is None:
            errors.append("Поле 'group' є обов'язковим")
        elif not isinstance(group, str) or not group.strip():
            errors.append("Поле 'group' має бути непорожнім рядком")
        else:
            cleaned['group'] = group.strip()

        email = data.get('email', '')
        if email and (not isinstance(email, str) or '@' not in email):
            errors.append("Поле 'email' має містити '@'")
        else:
            cleaned['email'] = email.strip() if email else ''

        gpa = data.get('gpa')
        if gpa is None:
            errors.append("Поле 'gpa' є обов'язковим")
        else:
            try:
                gpa = float(gpa)
                if gpa < 0 or gpa > 100:
                    errors.append("Поле 'gpa' має бути в діапазоні 0-100")
                else:
                    cleaned['gpa'] = gpa
            except (TypeError, ValueError):
                errors.append("Поле 'gpa' має бути числом")

        if errors:
            return None, errors
        return cleaned, []

    @staticmethod
    def serialize_list(students: list[dict], fields: list[str] | None = None) -> list[dict]:
        """Серіалізувати список студентів."""
        return [StudentSerializer.serialize(s, fields) for s in students]


# --- Middleware: логування запитів ---


@app.before_request
def log_request():
    """Логувати кожен вхідний запит."""
    g.start_time = time.time()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
          f"{request.method} {request.path} "
          f"IP: {request.remote_addr}")


@app.after_request
def add_headers(response):
    """Додати заголовки до кожної відповіді."""
    if hasattr(g, 'start_time'):
        elapsed = round((time.time() - g.start_time) * 1000, 2)
        response.headers['X-Request-Time'] = f"{elapsed}ms"

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-API-Key'

    return response


# --- Декоратор авторизації ---


def require_api_key(f):
    """Перевірка API-ключа у заголовку X-API-Key."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if api_key != "secret-api-key-123":
            return jsonify({
                "error": "Невірний API-ключ",
                "status": 401,
                "timestamp": datetime.now().isoformat()
            }), 401
        return f(*args, **kwargs)
    return wrapper


# --- Централізована обробка помилок ---


class APIError(Exception):
    """Базове виключення API."""
    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}


@app.errorhandler(APIError)
def handle_api_error(error):
    """Централізована обробка помилок API."""
    response = {
        "error": error.message,
        "status": error.status_code,
        "details": error.details,
        "timestamp": datetime.now().isoformat(),
    }
    return jsonify(response), error.status_code


# --- REST API ендпоінти ---


@app.route("/api/v2/students", methods=["GET"])
def get_students_v2():
    """GET /api/v2/students — з серіалізацією та вибором полів."""
    fields_param = request.args.get('fields')
    fields = [f.strip() for f in fields_param.split(',')] if fields_param else None

    search = request.args.get('search', '').strip().lower()

    sort_by = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc')

    students = list(students_db.values())

    if search:
        students = [s for s in students
                   if search in s['name'].lower()
                   or search in s['group'].lower()
                   or search in s.get('email', '').lower()]

    if sort_by in ['name', 'gpa', 'group']:
        reverse = (order == 'desc')
        students.sort(key=lambda x: x[sort_by], reverse=reverse)

    serialized = StudentSerializer.serialize_list(students, fields)

    return jsonify({
        "count": len(serialized),
        "students": serialized
    }), 200


@app.route("/api/v2/students", methods=["POST"])
@require_api_key
def create_student_v2():
    """POST /api/v2/students — з серіалізацією та авторизацією."""
    global next_id

    data = request.get_json(silent=True)

    cleaned, errors = StudentSerializer.deserialize(data)

    if errors:
        raise APIError(
            message="Помилка валідації",
            status_code=422,
            details={"fields": errors}
        )

    if cleaned.get('email'):
        for s in students_db.values():
            if s['email'].lower() == cleaned['email'].lower():
                raise APIError(
                    message=f"Email '{cleaned['email']}' вже використовується",
                    status_code=422
                )

    new_student = {
        "id": next_id,
        **cleaned,
        "created_at": datetime.now().isoformat()
    }

    students_db[next_id] = new_student
    next_id += 1

    serialized = StudentSerializer.serialize(new_student)

    return jsonify(serialized), 201


@app.route("/api/v2/students/<int:student_id>", methods=["GET"])
def get_student_v2(student_id):
    """GET /api/v2/students/:id — з серіалізацією."""
    student = students_db.get(student_id)
    if not student:
        raise APIError("Студента не знайдено", status_code=404)

    fields_param = request.args.get('fields')
    fields = [f.strip() for f in fields_param.split(',')] if fields_param else None

    serialized = StudentSerializer.serialize(student, fields)
    return jsonify(serialized), 200


# --- Обробка помилок ---


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Ресурс не знайдено",
        "status": 404,
        "timestamp": datetime.now().isoformat()
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Некоректний запит",
        "status": 400,
        "timestamp": datetime.now().isoformat()
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Метод не дозволено",
        "status": 405,
        "timestamp": datetime.now().isoformat()
    }), 405


# Тимчасове сховище
students_db = {}
next_id = 1


if __name__ == "__main__":
    test_students = [
        {"name": "Іваненко О.", "group": "КІ-21", "email": "ivan@kpi.ua", "gpa": 85.5},
        {"name": "Петренко М.", "group": "КІ-21", "email": "petro@kpi.ua", "gpa": 92.0},
        {"name": "Сидоренко А.", "group": "КІ-22", "email": "syd@kpi.ua", "gpa": 78.3},
        {"name": "Коваль Л.", "group": "КІ-22", "email": "koval@kpi.ua", "gpa": 95.1},
        {"name": "Яковенко К.", "group": "КІ-23", "email": "yakov@kpi.ua", "gpa": 88.5},
    ]
    for s in test_students:
        students_db[next_id] = {**s, "id": next_id,
                                 "created_at": datetime.now().isoformat()}
        next_id += 1

    app.run(debug=True, port=5000)