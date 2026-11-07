from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Блог на Flask</h1>'

@app.route('/api/posts')
def api_posts():
    posts = Post.query.filter_by(status='published').all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'slug': p.slug
    } for p in posts])

if __name__ == '__main__':
    app.run(debug=True)