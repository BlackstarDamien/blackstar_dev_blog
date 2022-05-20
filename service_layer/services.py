from adapters.repository import AbstractRepository
from domain.model import Article
from typing import List
from .exceptions import ArticleNotFound

def list_articles(repository: AbstractRepository) -> List[Article]:
    return repository.list_items()

def get_article(title: str, repository: AbstractRepository) -> Article:
    try:
        article = repository.get(title)
    except IndexError:
        raise ArticleNotFound(f"Article with title '{title}' not found.")
    return article

def add_article(new_article: Article, repository: AbstractRepository, session):
    repository.add(new_article)
    session.commit()
