import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify, request

from adapters import orm, repository
from service_layer import services, exceptions

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
        "reference": article.reference,
        "title": article.title,
        "author": article.author,
        "publication_date": str(article.publication_date),
        "description": article.description,
        "tags": [tag.name for tag in article.tags],
    } for article in articles]

    response = jsonify({"articles": articles})
    return response, 200

@app.route("/articles/<reference>")
def get_article(reference):
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)

    try:
        article = services.get_article(reference, repo)
    except exceptions.ArticleNotFound as e:
        return jsonify({"message": str(e)}), 404

    article_json = {
        "reference": article.reference,
        "title": article.title,
        "author": article.author,
        "publication_date": str(article.publication_date),
        "description": article.description,
        "tags": [tag.name for tag in article.tags],
        "content": article.content,
    }

    response = jsonify(article_json)
    return article_json, 200

@app.route("/articles", methods=['POST'])
def add_article():
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)
    try:
        services.add_article(request.json, repo, session)
    except exceptions.ArticleAlreadyExists as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Article was added"}), 201

@app.route("/articles/<reference>", methods=['PATCH'])
def edit_article(reference):
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)

    services.edit_article(reference, request.json, repo, session)

    return jsonify({"message": "Article successfully edited."}), 200
