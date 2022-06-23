from typing import List

from blog_service.adapters.repository import AbstractRepository
from blog_service.domain.model import Article, Tag

from .exceptions import ArticleAlreadyExists, ArticleNotFound
from .unit_of_work import AbstractUnitOfWork


def list_articles(uow: AbstractUnitOfWork) -> List[Article]:
    """Calls list_items() method of repository to fetch
    list of all available articles.

    Parameters
    ----------
    repository : AbstractRepository
        Repository with articles.

    Returns
    -------
    List[Article]
        List of available articles.
    """
    with uow:
        articles = uow.articles.list_items()
    return articles


def get_article(reference: str, uow: AbstractUnitOfWork) -> Article:
    """Calls get() method of repository to fetch article
    assigned to given reference.

    Parameters
    ----------
    reference : str
        Article's identifier.
    repository : AbstractRepository
        Repository with articles.

    Returns
    -------
    Article
        Article for given reference.

    Raises
    ------
    ArticleNotFound
        Raised when article was not found for given reference.
    """
    try:
        with uow:
            article = uow.articles.get(reference)
    except Exception:
        raise ArticleNotFound("Article not found.")
    return article


def add_article(new_article: dict, uow: AbstractUnitOfWork):
    """Creates new Article object by using provided dictioniary,
    generates and assign reference, and calls add() method of repository
    to add article into repository.

    Parameters
    ----------
    new_article : dict
        Defined properties for new article.
    repository : AbstractRepository
        Repository with articles.
    session :
        Session object

    Raises
    ------
    ArticleAlreadyExists
        Raised when article with the same reference exists.
    """
    articles = list_articles(uow)

    new_article["reference"] = uow.articles.next_reference(new_article["title"])
    if "tags" in new_article:
        new_article["tags"] = {Tag(tag) for tag in new_article["tags"]}

    new_article = Article(**new_article)
    if new_article in articles:
        raise ArticleAlreadyExists("Article already exists.")

    with uow:
        uow.articles.add(new_article)
        uow.commit()


def remove_article(reference: str, uow: AbstractUnitOfWork):
    """Calls remove() method of repository to remove article for given
    reference.

    Parameters
    ----------
    reference : str
        Article's identifier.
    repository : AbstractRepository
        Repository with articles.
    session :
        Session object

    Raises
    ------
    ArticleNotFound
        Raised when article was not found for given reference.
    """
    try:
        with uow:
            uow.articles.remove(reference)
            uow.commit()
    except Exception:
        raise ArticleNotFound("Article not found.")


def edit_article(reference: str, data: dict, uow: AbstractUnitOfWork):
    """Create scopy of article assigned with given reference, apply modifications
    from data dictionary and replaces old article with modified one.

    Parameters
    ----------
    reference : str
        Article's identifier.
    data : dict
        Properties with new values.
    repository : AbstractRepository
        Repository with articles.
    session :
        Session object
    """
    article = get_article(reference, uow)
    new_article = {
        "title": article.title,
        "author": article.author,
        "publication_date": str(article.publication_date),
        "description": article.description,
        "content": article.content,
        "tags": {tag.name for tag in article.tags},
    }

    for field in data:
        new_article[field] = data[field]

    with uow:
        remove_article(article.reference, uow)
        add_article(new_article, uow)
        uow.commit()
