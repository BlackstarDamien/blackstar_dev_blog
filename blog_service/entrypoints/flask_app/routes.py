from typing import Dict, List, Tuple

from blog_service.adapters import orm
from blog_service.service_layer import exceptions, services, unit_of_work
from flask import Blueprint, Flask, jsonify, request

articles_blueprint = Blueprint("articles_blueprint", __name__)


@articles_blueprint.route("/health")
def health_check() -> str:
    """Checks if API is up and running.

    Returns
    -------
    str
        HTML code that is rendered into page.
    """
    return """
        <center>
        <div>
            <h1>Hoooray! We are online!</h1>
            <img src="./static/kukulek.JPG">
        </div>
        </center>
    """


@articles_blueprint.route("/articles")
def get_articles() -> Tuple[Dict[str, List], int]:
    """Returns list of all available articles.

    Returns
    -------
    Tuple[Dict[str, List], int]
        All available articles and status code.
    """
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    articles = services.list_articles(uow)
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


@articles_blueprint.route("/articles/<reference>")
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
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    try:
        article = services.get_article(reference, uow)
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
    return jsonify(article_json), 200


@articles_blueprint.route("/articles", methods=["POST"])
def add_article() -> Tuple[dict, int]:
    """Adds new article.

    Returns
    -------
    Tuple[dict, int]
        Message with status code.
    """
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    try:
        services.add_article(request.json, uow)
    except exceptions.ArticleAlreadyExists as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Article was added"}), 201


@articles_blueprint.route("/articles/<reference>", methods=["PATCH"])
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
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    try:
        services.edit_article(reference, request.json, uow)
    except exceptions.ArticleNotFound as e:
        return jsonify({"message": str(e)}), 404

    return jsonify({"message": "Article successfully edited."}), 200


@articles_blueprint.route("/articles/<reference>", methods=["DELETE"])
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
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    try:
        services.remove_article(reference, uow)
    except exceptions.ArticleNotFound as e:
        return jsonify({"message": str(e)}), 404

    return jsonify({"message": "Article successfully removed."}), 200
