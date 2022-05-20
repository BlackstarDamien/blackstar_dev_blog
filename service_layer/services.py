from adapters.repository import AbstractRepository
from domain.model import Article
from typing import List

def list_articles(repository: AbstractRepository) -> List[Article]:
    return repository.list_items()

def get_article(title: str, repository: AbstractRepository) -> Article:
    return repository.get(title)
