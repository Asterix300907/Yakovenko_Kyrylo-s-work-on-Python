"""Маршрутизація Flask: GET, POST, динамічні параметри."""

from flask import Flask, request, render_template_string, redirect, url_for, abort

app = Flask(__name__)

# Шаблон HTML для демонстрації
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <nav>
        <a href="{{ url_for('index') }}">Головна</a> |
        <a href="{{ url_for('post_list') }}">Публікації</a> |
        <a href="{{ url_for('search') }}">Пошук</a>
    </nav>
    <hr>
    {{ content | safe }}
</body>
</html>
"""

# Тимчасове сховище даних
posts_db = [
    {"id": 1, "title": "Вступ до Python", "content": "Python — потужна мова...",
     "author": "Іван"},
    {"id": 2, "title": "Flask для початківців", "content": "Flask — мікрофреймворк...",
     "author": "Марія"},
    {"id": 3, "title": "REST API", "content": "REST — архітектурний стиль...",
     "author": "Петро"},
]
next_id = 4


# 1. Головна сторінка (GET /)
@app.route("/")
def index():
    html = """
    <p>Ласкаво просимо до блогу!</p>
    <p>Всього публікацій: <b>{}</b></p>
    """.format(len(posts_db))
    return render_template_string(BASE_TEMPLATE, title="Головна", content=html)


# 2. Список публікацій з пагінацією (GET /posts?page=1&per_page=10)
@app.route("/posts")
def post_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    start = (page - 1) * per_page
    end = start + per_page
    page_posts = posts_db[start:end]
    
    html = "<ul>"
    for p in page_posts:
        html += '<li><a href="{}">{}</a> — {}</li>'.format(
            url_for('post_detail', post_id=p['id']), p['title'], p['author']
        )
    html += "</ul>"
    html += "<p>Сторінка {} (показано {} з {})</p>".format(page, len(page_posts), len(posts_db))
    
    return render_template_string(BASE_TEMPLATE, title="Публікації", content=html)


# 3. Деталі публікації (GET /posts/<int:post_id>) — або 404
@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        abort(404)
    
    html = """
    <h2>{}</h2>
    <p><b>Автор:</b> {}</p>
    <p>{}</p>
    <a href="{}">← Назад до списку</a>
    """.format(post['title'], post['author'], post['content'], url_for('post_list'))
    
    return render_template_string(BASE_TEMPLATE, title=post['title'], content=html)


# 4. Створення публікації (GET+POST /posts/create)
@app.route("/posts/create", methods=["GET", "POST"])
def post_create():
    global next_id
    
    if request.method == "POST":
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '').strip()
        
        if not title or not content:
            html = "<p style='color:red'>Помилка: заповніть заголовок та контент!</p>"
            html += """
            <form method="POST">
                <p>Заголовок: <input type="text" name="title" value="{}"></p>
                <p>Автор: <input type="text" name="author" value="{}"></p>
                <p>Контент: <textarea name="content" rows="5" cols="40">{}</textarea></p>
                <p><button type="submit">Створити</button></p>
            </form>
            """.format(title, author, content)
            return render_template_string(BASE_TEMPLATE, title="Створити публікацію", content=html)
        
        new_post = {
            "id": next_id,
            "title": title,
            "content": content,
            "author": author
        }
        posts_db.append(new_post)
        next_id += 1
        
        return redirect(url_for('post_detail', post_id=new_post['id']))
    
    # GET — показати форму
    html = """
    <form method="POST">
        <p>Заголовок: <input type="text" name="title" required></p>
        <p>Автор: <input type="text" name="author"></p>
        <p>Контент: <textarea name="content" rows="5" cols="40" required></textarea></p>
        <p><button type="submit">Створити</button></p>
    </form>
    """
    return render_template_string(BASE_TEMPLATE, title="Створити публікацію", content=html)


# 5. Пошук (GET /search?q=query)
@app.route("/search")
def search():
    q = request.args.get('q', '').strip().lower()
    
    if not q:
        html = """
        <form method="GET">
            <p>Пошук: <input type="text" name="q" placeholder="Введіть запит..."></p>
            <p><button type="submit">Шукати</button></p>
        </form>
        """
        return render_template_string(BASE_TEMPLATE, title="Пошук", content=html)
    
    results = [p for p in posts_db if q in p['title'].lower() or q in p['content'].lower()]
    
    html = "<p>Результати пошуку для '<b>{}</b>': знайдено {}</p><ul>".format(q, len(results))
    for p in results:
        html += '<li><a href="{}">{}</a> — {}</li>'.format(
            url_for('post_detail', post_id=p['id']), p['title'], p['author']
        )
    html += "</ul>"
    
    return render_template_string(BASE_TEMPLATE, title="Результати пошуку", content=html)


# 6. Архів за датою (GET /archive/<int:year>/<int:month>)
@app.route("/archive/<int:year>/<int:month>")
def archive(year, month):
    html = """
    <p>Архів публікацій за <b>{}/{}</b></p>
    <p>У цьому архіві поки що немає публікацій (демо-режим).</p>
    <p>Всі публікації блогу:</p>
    <ul>
    """.format(year, month)
    for p in posts_db:
        html += '<li><a href="{}">{}</a></li>'.format(
            url_for('post_detail', post_id=p['id']), p['title']
        )
    html += "</ul>"
    
    return render_template_string(BASE_TEMPLATE, title="Архів", content=html)


# 7. Профіль користувача (GET /user/<username>)
@app.route("/user/<username>")
def user_profile(username):
    user_posts = [p for p in posts_db if p['author'].lower() == username.lower()]
    
    html = "<p>Профіль користувача: <b>{}</b></p>".format(username)
    html += "<p>Кількість публікацій: {}</p><ul>".format(len(user_posts))
    for p in user_posts:
        html += '<li><a href="{}">{}</a></li>'.format(
            url_for('post_detail', post_id=p['id']), p['title']
        )
    html += "</ul>"
    
    return render_template_string(BASE_TEMPLATE, title="Профіль: {}".format(username), content=html)


if __name__ == "__main__":
    app.run(debug=True, port=5000)