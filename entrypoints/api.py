import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask

from adapters import orm, repository

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/health")
def health_check():
    return "<h1>Hoooray! We are online!</h1>"


@app.route("/articles")
def get_articles():
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)
    articles = repo.list_items()

    return articles, 200
