"""CRUD: Update та Delete для блогу."""

from flask import Flask, request, render_template_string, redirect, url_for, flash, abort
from datetime import datetime

app = Flask(__name__)
app.secret_key = "blog-secret-key"

# HTML-шаблони
LIST_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Блог</title></head>
<body>
    <h1>Публікації</h1>
    {% with messages = get_flashed_messages() %}
    {% if messages %}<div style="color: green;">{{ messages[0] }}</div>{% endif %}
    {% endwith %}
    <a href="{{ url_for('post_create') }}">+ Нова публікація</a>
    <hr>
    {% for post in posts %}
    <article>
        <h2><a href="{{ url_for('post_detail', post_id=post.id) }}">{{ post.title }}</a></h2>
        <p>{{ post.content[:100] }}...</p>
        <small>{{ post.author }} | {{ post.created_at }}</small>
        <br>
        <a href="{{ url_for('post_edit', post_id=post.id) }}">Редагувати</a> |
        <a href="{{ url_for('post_delete', post_id=post.id) }}" style="color: red;">Видалити</a>
    </article>
    <hr>
    {% endfor %}
    {% if not posts %}
    <p>Публікацій ще немає. <a href="{{ url_for('post_create') }}">Створіть першу!</a></p>
    {% endif %}
</body>
</html>
"""

DETAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ post.title }}</title></head>
<body>
    <h1>{{ post.title }}</h1>
    <p><b>Автор:</b> {{ post.author }}</p>
    <p><b>Опубліковано:</b> {{ post.created_at }}</p>
    <hr>
    <p>{{ post.content }}</p>
    <hr>
    <a href="{{ url_for('post_edit', post_id=post.id) }}">Редагувати</a> |
    <a href="{{ url_for('post_delete', post_id=post.id) }}" style="color: red;">Видалити</a> |
    <a href="{{ url_for('post_list') }}">← Назад до списку</a>
</body>
</html>
"""

FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ form_title }}</title></head>
<body>
    <h1>{{ form_title }}</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
        <div style="color: {% if category == 'error' %}red{% else %}green{% endif %};">{{ message }}</div>
        {% endfor %}
    {% endif %}
    {% endwith %}
    <form method="POST">
        <label>Заголовок:</label><br>
        <input type="text" name="title" value="{{ post.title if post else '' }}"
               required style="width:400px;"><br><br>
        <label>Автор:</label><br>
        <input type="text" name="author" value="{{ post.author if post else '' }}"
               required><br><br>
        <label>Зміст:</label><br>
        <textarea name="content" rows="10" cols="50"
                  required>{{ post.content if post else '' }}</textarea><br><br>
        <button type="submit">{{ button_text }}</button>
        <a href="{{ url_for('post_list') }}">Скасувати</a>
    </form>
</body>
</html>
"""

DELETE_CONFIRM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Видалення</title></head>
<body>
    <h1>Підтвердження видалення</h1>
    <p>Ви дійсно бажаєте видалити публікацію "<strong>{{ post.title }}</strong>"?</p>
    <p><i>Цю дію неможливо буде скасувати.</i></p>
    <form method="POST">
        <button type="submit" style="color: red; font-weight: bold;">Так, видалити</button>
        <a href="{{ url_for('post_detail', post_id=post.id) }}">Скасувати</a>
    </form>
</body>
</html>
"""


@app.route("/posts")
def post_list():
    """READ: список усіх публікацій."""
    return render_template_string(LIST_TEMPLATE, posts=posts_db)


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    """READ: деталі однієї публікації."""
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        abort(404)
    return render_template_string(DETAIL_TEMPLATE, post=post)


@app.route("/posts/create", methods=["GET", "POST"])
def post_create():
    """CREATE: створення нової публікації."""
    global next_id
    
    if request.method == "POST":
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not author or not content:
            flash('Помилка: всі поля обов\'язкові для заповнення!', 'error')
            return render_template_string(
                FORM_TEMPLATE,
                form_title="Створити публікацію",
                button_text="Створити",
                post={'title': title, 'author': author, 'content': content}
            )
        
        new_post = {
            'id': next_id,
            'title': title,
            'author': author,
            'content': content,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        posts_db.append(new_post)
        next_id += 1
        
        flash(f'Публікацію "{title}" успішно створено!')
        return redirect(url_for('post_detail', post_id=new_post['id']))
    
    return render_template_string(
        FORM_TEMPLATE,
        form_title="Створити публікацію",
        button_text="Створити",
        post=None
    )


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def post_edit(post_id):
    """UPDATE: редагування публікації."""
    # Знаходимо публікацію за ID
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        abort(404)
    
    if request.method == "POST":
        # Зчитуємо дані з форми
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()
        
        # Валідація: перевірка на непорожні поля
        if not title or not author or not content:
            flash('Помилка: всі поля обов\'язкові для заповнення!', 'error')
            return render_template_string(
                FORM_TEMPLATE,
                form_title="Редагувати публікацію",
                button_text="Зберегти зміни",
                post={'title': title, 'author': author, 'content': content}
            )
        
        # Оновлюємо публікацію
        post['title'] = title
        post['author'] = author
        post['content'] = content
        
        flash(f'Публікацію "{title}" успішно оновлено!')
        return redirect(url_for('post_detail', post_id=post['id']))
    
    # GET — показуємо форму з поточними даними
    return render_template_string(
        FORM_TEMPLATE,
        form_title="Редагувати публікацію",
        button_text="Зберегти зміни",
        post=post
    )


@app.route("/posts/<int:post_id>/delete", methods=["GET", "POST"])
def post_delete(post_id):
    """DELETE: видалення публікації з підтвердженням."""
    # Знаходимо публікацію за ID
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        abort(404)
    
    if request.method == "POST":
        # Видаляємо публікацію
        title = post['title']
        posts_db.remove(post)
        
        flash(f'Публікацію "{title}" видалено.')
        return redirect(url_for('post_list'))
    
    # GET — показуємо сторінку підтвердження
    return render_template_string(DELETE_CONFIRM_TEMPLATE, post=post)


# Тимчасове сховище
posts_db = [
    {"id": 1, "title": "Перша публікація", "content": "Зміст першої публікації...",
     "author": "Іван", "created_at": "2025-01-15"},
    {"id": 2, "title": "Друга публікація", "content": "Зміст другої публікації...",
     "author": "Марія", "created_at": "2025-01-20"},
]
next_id = 3


if __name__ == "__main__":
    app.run(debug=True, port=5000)