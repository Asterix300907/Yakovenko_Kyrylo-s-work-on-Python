"""Головний файл Flask-додатка."""

from flask import Flask, jsonify, request

from config import config_by_name


def create_app(config_name: str = 'default') -> Flask:
    """Фабрика додатка Flask.

    Args:
        config_name: ім'я конфігурації ('development', 'production').

    Returns:
        Налаштований екземпляр Flask.
    """
    app = Flask(__name__)

    # Завантажити конфігурацію
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Зареєструвати маршрути
    register_routes(app)

    return app


def register_routes(app: Flask):
    """Реєструє маршрути додатка."""

    @app.route('/')
    def index():
        """Головна сторінка."""
        return """
        <h1>Ласкаво просимо до Flask-додатку!</h1>
        <p>Це головна сторінка.</p>
        <ul>
            <li><a href="/about">Про додаток</a></li>
            <li><a href="/api/info">API інформація (JSON)</a></li>
            <li><a href="/greet">Привітання</a></li>
            <li><a href="/greet/Кирило">Привітання з ім'ям</a></li>
        </ul>
        """

    @app.route('/about')
    def about():
        """Сторінка 'Про додаток'."""
        return """
        <h1>Про додаток</h1>
        <p><strong>Фреймворк:</strong> Flask</p>
        <p><strong>Дисципліна:</strong> Програмування</p>
        <p><strong>Практична робота:</strong> №5</p>
        <p><strong>Виконав:</strong> Яковенко Кирило, група БІКСб-12-540</p>
        """

    @app.route('/api/info')
    def api_info():
        """API-ендпоінт з інформацією у JSON."""
        routes = [rule.rule for rule in app.url_map.iter_rules()
                  if rule.endpoint != 'static']
        return jsonify({
            'framework': 'Flask',
            'version': '3.1.3',
            'debug': app.config.get('DEBUG', False),
            'routes': routes
        })

    @app.route('/greet')
    @app.route('/greet/<name>')
    def greet(name=None):
        """Маршрут з динамічним параметром та query-параметром."""
        if name is None:
            name = request.args.get('name', 'Гість')
        return f"<h1>Привіт, {name}!</h1><p>Радий бачити тебе у Flask-додатку.</p>"


if __name__ == '__main__':
    application = create_app('development')
    application.run(debug=True, port=5000)