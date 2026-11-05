"""Views додатка pages."""

from django.http import HttpResponse


def index(request):
    """Головна сторінка."""
    html = """
    <h1>Ласкаво просимо до мого Django-проекту!</h1>
    <p>Це головна сторінка додатка pages.</p>
    <ul>
        <li>Пункт 1: Вивчення основ Django</li>
        <li>Пункт 2: Налаштування маршрутизації (URLs)</li>
        <li>Пункт 3: Робота з Views та HTTP-запитами</li>
    </ul>
    """
    return HttpResponse(html)


def about(request):
    """Сторінка 'Про проект'."""
    html = """
    <h1>Про проект</h1>
    <p><strong>Дисципліна:</strong> Програмування</p>
    <p><strong>Практична робота:</strong> №5</p>
    <p><strong>Виконав:</strong> Яковенко Кирило, група БІКСб-12-540</p>
    """
    return HttpResponse(html)


def contact(request):
    """Контактна сторінка з параметрами запиту."""
    name = request.GET.get('name')
    if name:
        html = f"<h1>Привіт, {name}!</h1><p>Радий бачити тебе на контактній сторінці.</p>"
    else:
        html = "<h1>Контактна сторінка</h1><p>Будь ласка, додайте параметр <code>?name=Ваше_Ім'я</code> до URL, щоб отримати персональне привітання.</p>"
    return HttpResponse(html)