from adapters.repository import AbstractRepository
from domain.model import Article
from typing import List
from .exceptions import ArticleNotFound, ArticleAlreadyExists

def list_articles(repository: AbstractRepository) -> List[Article]:
    return repository.list_items()

def get_article(title: str, repository: AbstractRepository) -> Article:
    try:
        article = repository.get(title)
    except IndexError:
        raise ArticleNotFound(f"Article with title '{title}' not found.")
    return article

def add_article(new_article: Article, repository: AbstractRepository, session):
    articles = list_articles(repository)
    if new_article in articles:
        raise ArticleAlreadyExists(f"Article with title '{new_article.title}' already exists.")

    repository.add(new_article)
    session.commit()

def remove_article(title: str, repository: AbstractRepository, session):
    repository.remove(title)
    session.commit()
