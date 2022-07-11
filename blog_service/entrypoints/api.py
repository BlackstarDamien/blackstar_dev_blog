from blog_service.adapters import orm
from flask import Flask


def create_app():
    orm.start_mappers()
    app = Flask(__name__)

    with app.app_context():
        from .flask_app.routes import articles_blueprint

        app.register_blueprint(articles_blueprint)

        return app
