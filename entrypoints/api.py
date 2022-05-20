import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify

from adapters import orm, repository
from service_layer import services

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/health")
def health_check():
    return """
        <center><div>
            <h1>Hoooray! We are online!</h1>
            <img src="https://img.xcitefun.net/users/2009/05/59593,xcitefun-download10.jpg">
        </div></center>
    """


@app.route("/articles")
def get_articles():
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)
    articles = services.list_articles(repo)
    articles = [{
        "title": article.title,
        "author": article.author,
        "publication_date": str(article.publication_date),
        "description": article.description,
        "tags": [tag.name for tag in article.tags],
        "content": article.content,
    } for article in articles]

    response = jsonify({"articles": articles})
    return response, 200
