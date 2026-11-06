"""Flask блог — головний файл."""
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError 
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


# ============================================================
# ФОРМА ЗВОРОТНОГО ЗВ'ЯЗКУ (Flask-WTF)
# ============================================================
class FeedbackForm(FlaskForm):
    """Форма зворотного зв'язку з валідацією."""

    name = StringField(
        "Ваше ім'я та прізвище",
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення."),
            Length(min=2, max=50, message="Ім'я має містити від 2 до 50 символів.")
        ],
        render_kw={"placeholder": "Наприклад: Іван Петренко"}
    )

    email = EmailField(
        "Електронна пошта",
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення."),
            Email(message="Введіть коректну електронну адресу.")
        ],
        render_kw={"placeholder": "example@mail.com"}
    )

    subject = SelectField(
        "Тема звернення",
        choices=[
            ('general', 'Загальне питання'),
            ('support', 'Технічна підтримка'),
            ('feedback', 'Відгук про сайт'),
        ],
        validators=[DataRequired(message="Оберіть тему звернення.")]
    )

    message = TextAreaField(
        "Ваше повідомлення",
        validators=[
            DataRequired(message="Поле обов'язкове для заповнення."),
            Length(min=10, message="Повідомлення має містити щонайменше 10 символів.")
        ],
        render_kw={"rows": 5, "placeholder": "Опишіть ваше питання детально..."}
    )

    submit = SubmitField("Надіслати повідомлення")

    # Кастомна валідація для поля name
    def validate_name(self, field):
        if len(field.data.split()) < 2:
            raise ValidationError("Будь ласка, введіть повне ім'я та прізвище (мінімум 2 слова).")

    # Кастомна валідація для поля message
    def validate_message(self, field):
        if len(field.data.split()) < 5:
            raise ValidationError("Повідомлення має містити щонайменше 5 слів.")


# ============================================================
# МАРШРУТИ
# ============================================================
@app.route('/')
def index():
    return render_template(
        'index.html',
        site_name='Мій Flask Блог',
        posts_count=3,
        multiplier=2,
        description='Це найкращий блог про програмування на Python, створений за допомогою Flask.'
    )


@app.route('/posts')
def posts():
    posts_list = [
        {'title': 'Вступ до Python', 'author': 'Кирило', 'date': '2026-11-01', 'content': 'Python це інтерпретована мова програмування високого рівня. Вона дуже популярна.'},
        {'title': 'Основи Flask', 'author': 'Іван', 'date': '2026-11-05', 'content': 'Flask це мікрофреймворк, який дає свободу вибору інструментів.'},
        {'title': 'Пустий пост', 'author': 'Оля', 'date': '2026-11-06', 'content': ''},
    ]
    return render_template('posts.html', site_name='Мій Flask Блог', posts=posts_list)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Обробка форми зворотного зв'язку."""
    form = FeedbackForm()

    if form.validate_on_submit():
        # Успішна валідація
        user_name = form.name.data
        flash(f"Дякуємо, {user_name}! Ваше повідомлення успішно надіслано. Ми відповімо вам найближчим часом.", "success")
        return redirect(url_for('contact'))

    # GET-запит або невалідна форма — рендеримо шаблон з формою
    return render_template('contact.html', form=form, site_name='Мій Flask Блог')


if __name__ == '__main__':
    app.run(debug=True)