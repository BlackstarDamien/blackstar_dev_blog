from adapters.repository import AbstractRepository
from domain.model import Article, Tag
from typing import List
from .exceptions import ArticleNotFound, ArticleAlreadyExists
from copy import deepcopy

def list_articles(repository: AbstractRepository) -> List[Article]:
    return repository.list_items()

def get_article(title: str, repository: AbstractRepository) -> Article:
    try:
        article = repository.get(title)
    except Exception:
        raise ArticleNotFound(f"Article with title '{title}' not found.")
    return article

def add_article(new_article: dict, repository: AbstractRepository, session):
    articles = list_articles(repository)

    if 'tags' in new_article:
        new_article["tags"] = {Tag(tag) for tag in new_article["tags"]}

    new_article = Article(**new_article)
    if new_article in articles:
        raise ArticleAlreadyExists(f"Article with title '{new_article.title}' already exists.")

    repository.add(new_article)
    session.commit()

def remove_article(title: str, repository: AbstractRepository, session):
    repository.remove(title)
    session.commit()

def edit_article(title: str, data: dict, repository: AbstractRepository, session):
    article = get_article(title, repository)
    new_article = {
        "title": article.title,
        "author": article.author,
        "publication_date": str(article.publication_date),
        "description": article.description,
        "content": article.content,
        "tags": article.tags,
    }

    for field in data:
        new_article[field] = data[field]

    remove_article(article.title, repository, session)
    add_article(new_article, repository, session)
    session.commit()
