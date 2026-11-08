"""CRUD: Create та Read для блогу."""

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
    </article>
    <hr>
    {% endfor %}
    {% if pagination %}
    <div>
        Сторінка {{ pagination.current_page }} з {{ pagination.total_pages }}
        {% if pagination.has_prev %}
        <a href="{{ url_for('post_list', page=pagination.prev) }}">← Попередня</a>
        {% endif %}
        {% if pagination.has_next %}
        <a href="{{ url_for('post_list', page=pagination.next) }}">Наступна →</a>
        {% endif %}
    </div>
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


@app.route("/posts")
def post_list():
    """READ: список усіх публікацій з пагінацією."""
    # Отримуємо номер сторінки з параметрів запиту
    page = request.args.get('page', 1, type=int)
    per_page = 5  # кількість постів на сторінку
    
    # Обчислюємо індекси для пагінації
    total_posts = len(posts_db)
    total_pages = (total_posts + per_page - 1) // per_page
    
    # Перевіряємо, чи сторінка в межах
    if page < 1:
        page = 1
    elif page > total_pages and total_posts > 0:
        abort(404)
    
    start = (page - 1) * per_page
    end = start + per_page
    page_posts = posts_db[start:end]
    
    # Формуємо дані для пагінації
    pagination = {
        'current_page': page,
        'total_pages': total_pages if total_pages > 0 else 1,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev': page - 1,
        'next': page + 1
    }
    
    return render_template_string(LIST_TEMPLATE, posts=page_posts, pagination=pagination)


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
        # Зчитуємо дані з форми
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()
        
        # Валідація: перевірка на непорожні поля
        if not title or not author or not content:
            flash('Помилка: всі поля обов\'язкові для заповнення!', 'error')
            return render_template_string(
                FORM_TEMPLATE, 
                form_title="Створити публікацію",
                button_text="Створити",
                post={'title': title, 'author': author, 'content': content}
            )
        
        # Створюємо нову публікацію
        new_post = {
            'id': next_id,
            'title': title,
            'author': author,
            'content': content,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        posts_db.append(new_post)
        next_id += 1
        
        # Flash-повідомлення про успіх
        flash(f'Публікацію "{title}" успішно створено!')
        
        # Перенаправляємо до деталей нової публікації (Post/Redirect/Get)
        return redirect(url_for('post_detail', post_id=new_post['id']))
    
    # GET — показуємо порожню форму
    return render_template_string(
        FORM_TEMPLATE, 
        form_title="Створити публікацію",
        button_text="Створити",
        post=None
    )


# Тимчасове сховище
posts_db = []
next_id = 1


if __name__ == "__main__":
    app.run(debug=True, port=5000)