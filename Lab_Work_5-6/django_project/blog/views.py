from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from datetime import datetime
from .forms import FeedbackForm

def index(request):
    """Головна сторінка зі статистикою."""
    context = {
        'site_name': 'Мій Django Блог',
        'posts_count': 3,
        'current_year': datetime.now().year,
        'description': 'Це найкращий блог про програмування на Python, створений за допомогою Django.',
    }
    return render(request, 'blog/index.html', context)

def posts(request):
    """Сторінка зі списком статей."""
    posts_list = [
        {
            'title': 'Вступ до Python',
            'author': 'Кирило',
            'date': '2026-11-01',
            'content': 'Python це інтерпретована мова програмування високого рівня. Вона дуже популярна.'
        },
        {
            'title': 'Основи Django',
            'author': 'Іван',
            'date': '2026-11-05',
            'content': 'Django це веб-фреймворк, який дозволяє швидко створювати складні сайти.'
        },
        {
            'title': 'Пустий пост',
            'author': 'Оля',
            'date': '2026-11-06',
            'content': '' 
        },
    ]
    context = {
        'site_name': 'Мій Django Блог',
        'posts': posts_list,
    }
    return render(request, 'blog/posts.html', context)

def contact(request):
    """Обробка форми зворотного зв'язку."""
    if request.method == 'POST':
        # При POST заповнюємо форму даними з запиту
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Якщо валідація пройшла успішно
            user_name = form.cleaned_data['name']
            messages.success(request, f"Дякуємо, {user_name}! Ваше повідомлення успішно надіслано. Ми відповімо вам найближчим часом.")
            return redirect('contact')  # Redirect після успішної відправки (Post/Redirect/Get паттерн)
    else:
        # При GET показуємо порожню форму
        form = FeedbackForm()

    return render(request, 'blog/contact.html', {'form': form, 'site_name': 'Мій Django Блог'})