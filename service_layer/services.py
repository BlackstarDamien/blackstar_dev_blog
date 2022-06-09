from adapters.repository import AbstractRepository
from domain.model import Article, Tag
from typing import List
from .exceptions import ArticleNotFound, ArticleAlreadyExists
from copy import deepcopy

def list_articles(repository: AbstractRepository) -> List[Article]:
    return repository.list_items()

def get_article(reference: str, repository: AbstractRepository) -> Article:
    try:
        article = repository.get(reference)
    except Exception:
        raise ArticleNotFound(f"Article not found.")
    return article

def add_article(new_article: dict, repository: AbstractRepository, session):
    articles = list_articles(repository)

    new_article["reference"] = repository.next_reference(new_article["title"])
    if 'tags' in new_article:
        new_article["tags"] = {Tag(tag) for tag in new_article["tags"]}

    new_article = Article(**new_article)
    if new_article in articles:
        raise ArticleAlreadyExists(f"Article already exists.")

    repository.add(new_article)
    session.commit()

def remove_article(reference: str, repository: AbstractRepository, session):
    try:
        repository.remove(reference)
    except Exception:
        raise ArticleNotFound(f"Article not found.")

    session.commit()

def edit_article(reference: str, data: dict, repository: AbstractRepository, session):
    article = get_article(reference, repository)
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

    remove_article(article.reference, repository, session)
    add_article(new_article, repository, session)
    session.commit()
