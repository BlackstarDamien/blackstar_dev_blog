import pytest

from adapters.repository import AbstractRepository
from domain.model import Article, Tag
from typing import List
from datetime import date
from service_layer import services, exceptions

class FakeRepository(AbstractRepository):
    def __init__(self, articles: List[Article]):
        self.articles = set(articles)

    def add(self, article: Article):
        return self.articles.add(article)

    def get(self, title: str) -> Article:
        article = [article for article in self.articles if article.title == title]
        return article[0]

    def list_items(self) -> List[Article]:
        return list(self.articles)

def prepare_fake_repo_with_data():
    article_jenkins = Article(
        "Importance of using CI/CD",
        "Tom Smith",
        date(2022, 4, 15),
        "Interesting stuff about CI/CD",
        "Something Something",
        {Tag("CI"), Tag("Jenkins")},
    )
    article_python = Article(
        "Design Patterns in Python",
        "Carl Johnson",
        date(2022, 2, 23),
        "Introduction into design patterns in Python",
        "Something Something",
    )
    article_rust = Article(
        "Design Virtual Machine in Rust",
        "Miles Kane",
        date(2021, 12, 15),
        "In this article we will create basic virtual machine in Rust",
        "Something Something",
    )
    repo = FakeRepository([article_jenkins, article_python, article_rust])
    return repo


def test_returns_all_articles():
    repo = prepare_fake_repo_with_data()
    articles = services.list_articles(repo)

    expected = set([article_jenkins, article_python, article_rust])
    assert not set(articles) ^ expected

def test_get_single_article():
    repo = prepare_fake_repo_with_data()
    article = services.get_article("Design Patterns in Python", repo)

    assert article == article_python

def test_should_throw_exception_when_article_is_not_found():
    with pytest.raises(exceptions.ArticleNotFound):
        repo = prepare_fake_repo_with_data()
        services.get_article("Some nonexistent article", repo)
