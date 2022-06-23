from typing import Dict, List, Tuple

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blog_service import config
from blog_service.adapters import orm, repository
from blog_service.service_layer import exceptions, services

orm.start_mappers()
get_session = sessionmaker(
    bind=create_engine(config.get_postgres_uri(), pool_pre_ping=True)
)
app = Flask(__name__)


@app.route("/health")
def health_check() -> str:
    """Checks if API is up and running.

    Returns
    -------
    str
        HTML code that is rendered into page.
    """
    return """
        <center><div>
            <h1>Hoooray! We are online!</h1>
            <img src="https://img.xcitefun.net/users/2009/05/59593,xcitefun-download10.jpg">
        </div></center>
    """


@app.route("/articles")
def get_articles() -> Tuple[Dict[str, List], int]:
    """Returns list of all available articles.

    Returns
    -------
    Tuple[Dict[str, List], int]
        All available articles and status code.
    """
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)
    articles = services.list_articles(repo)
    articles = [
        {
            "reference": article.reference,
            "title": article.title,
            "author": article.author,
            "publication_date": str(article.publication_date),
            "description": article.description,
            "tags": [tag.name for tag in article.tags],
        }
        for article in articles
    ]

    response = jsonify({"articles": articles})
    return response, 200


@app.route("/articles/<reference>")
def get_article(reference: str) -> Tuple[Dict, int]:
    """Returns article for given reference.

    Parameters
    ----------
    reference : str
        Article's identifier.

    Returns
    -------
    Tuple[Dict, int]
        Found article with status code.
    """
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


@app.route("/articles", methods=["POST"])
def add_article() -> Tuple[dict, int]:
    """Adds new article.

    Returns
    -------
    Tuple[dict, int]
        Message with status code.
    """
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)

    try:
        services.add_article(request.json, repo, session)
    except exceptions.ArticleAlreadyExists as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Article was added"}), 201


@app.route("/articles/<reference>", methods=["PATCH"])
def edit_article(reference: str) -> Tuple[dict, int]:
    """Allows to edit article associated to given reference.

    Parameters
    ----------
    reference : str
        Article's identifier.

    Returns
    -------
    Tuple[dict, int]
        Message with status code.
    """
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)

    try:
        services.edit_article(reference, request.json, repo, session)
    except exceptions.ArticleNotFound as e:
        return jsonify({"message": str(e)}), 404

    return jsonify({"message": "Article successfully edited."}), 200


@app.route("/articles/<reference>", methods=["DELETE"])
def remove_article(reference: str) -> Tuple[dict, int]:
    """Allow to remove article associated to given reference.

    Parameters
    ----------
    reference : str
        Article's identifier.

    Returns
    -------
    Tuple[dict, int]
        Message with status code.
    """
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)

    try:
        services.remove_article(reference, repo, session)
    except exceptions.ArticleNotFound as e:
        return jsonify({"message": str(e)}), 404

    return jsonify({"message": "Article successfully removed."}), 200
