from copy import deepcopy
from datetime import date
from typing import List

import pytest
from blog_service.adapters.repository import AbstractRepository
from blog_service.domain.model import Article, Tag
from blog_service.service_layer import exceptions, services, unit_of_work

article_jenkins = Article(
    "importance-of-using-cdcd",
    "Importance of using CI/CD",
    "Tom Smith",
    date(2022, 4, 15),
    "Interesting stuff about CI/CD",
    "Something Something",
    {Tag("CI"), Tag("Jenkins")},
)

article_python = Article(
    "design-patterns-in-python",
    "Design Patterns in Python",
    "Carl Johnson",
    date(2022, 2, 23),
    "Introduction into design patterns in Python",
    "Something Something",
)

article_rust = Article(
    "design-virtual-machine-in-rust",
    "Design Virtual Machine in Rust",
    "Miles Kane",
    date(2021, 12, 15),
    "In this article we will create basic virtual machine in Rust",
    "Something Something",
)


class FakeRepository(AbstractRepository):
    def __init__(self, articles: List[Article]):
        self.articles = set(articles)

    def add(self, article: Article):
        return self.articles.add(article)

    def get(self, reference: str) -> Article:
        article = [
            article for article in self.articles if article.reference == reference
        ]
        return article[0]

    def list_items(self) -> List[Article]:
        return list(self.articles)

    def remove(self, reference: str):
        if not any([x for x in self.list_items() if x.reference == reference]):
            raise Exception

        self.articles = set(
            [article for article in self.articles if article.reference != reference]
        )

    def next_reference(self, custom_field: str) -> str:
        slug_title = custom_field.lower()
        slug_title = slug_title.replace(" ", "-")
        return slug_title


class FakeSession:
    def __init__(self):
        self.commited = False

    def commit(self):
        self.commited = True


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.articles = FakeRepository([article_jenkins, article_python, article_rust])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_returns_all_articles():
    """Tests that list_articles() is able to show all available
    articles.
    """
    uow = FakeUnitOfWork()
    articles = services.list_articles(uow)

    expected = set([article_jenkins, article_python, article_rust])
    assert not set(articles) ^ expected


def test_get_single_article():
    """Tests that get_article() is able to return article
    for given identifier.
    """
    uow = FakeUnitOfWork()
    article = services.get_article("design-patterns-in-python", uow)

    assert article == article_python


def test_should_throw_exception_when_article_is_not_found():
    """Tests that get_article() is able to throw exception
    when article for given identifier is not found.
    """
    uow = FakeUnitOfWork()
    with pytest.raises(exceptions.ArticleNotFound):
        services.get_article("Some nonexistent article", uow)


def test_should_add_new_article():
    """Tests that add_article() is able to add new article
    into repository.
    """
    uow = FakeUnitOfWork()
    new_article = {
        "title": "How to avoid loops in Python",
        "author": "Some Cool Programmer",
        "publication_date": "15-04-2022",
        "description": "In this article I'm telling how to optimize your code without loops",
        "content": "Something Something",
    }
    services.add_article(new_article, uow)

    fetched_article = services.get_article("how-to-avoid-loops-in-python", uow)

    expected_article = deepcopy(new_article)
    expected_article["reference"] = "how-to-avoid-loops-in-python"
    expected_article = Article(**expected_article)

    assert fetched_article == expected_article


def test_add_article_should_throw_exception_when_article_exists():
    """Tests that add_article() is able to throw an exception
    when trying to add article that already exists in repo.
    """
    uow = FakeUnitOfWork()
    article_rust = {
        "title": "Design Virtual Machine in Rust",
        "author": "Miles Kane",
        "publication_date": "15-12-2021",
        "description": "In this article we will create basic virtual machine in Rust",
        "content": "Something Something",
    }
    with pytest.raises(exceptions.ArticleAlreadyExists):
        services.add_article(article_rust, uow)


def test_should_remove_article():
    """Tests that remove_article() is able to fully delete
    article for given identifier from repo.
    """
    uow = FakeUnitOfWork()
    article_to_remove = "design-virtual-machine-in-rust"
    services.remove_article(article_to_remove, uow)

    with pytest.raises(exceptions.ArticleNotFound):
        services.get_article(article_to_remove, uow)


def test_remove_article_should_throw_exception():
    """Tests that remove_article() throws exception
    when trying to remove nonexistent article from repo.
    """
    uow = FakeUnitOfWork()
    with pytest.raises(exceptions.ArticleNotFound):
        services.remove_article("Some nonexistent article", uow)


def test_should_edit_existing_article():
    """Tests that edit_article() is able to edit existing article
    with provided new values for given fields.
    """
    uow = FakeUnitOfWork()
    fields_to_change = {
        "title": "Build Virtual Machine in Rust",
        "content": "Lorem ipsum Test Foo Something",
    }
    article_to_edit = "design-virtual-machine-in-rust"
    services.edit_article(article_to_edit, fields_to_change, uow)

    changed_article = services.get_article("build-virtual-machine-in-rust", uow)

    assert changed_article.title == fields_to_change["title"]
    assert changed_article.content == fields_to_change["content"]


def test_should_throw_exception_when_edit_missing_article():
    """Tests that edit_article() is able to throw exception when
    article to edit does not exist inside repo.
    """
    uow = FakeUnitOfWork()
    fields_to_change = {
        "title": "Build Virtual Machine in Rust",
        "content": "Lorem ipsum Test Foo Something",
    }
    article_to_edit = "Some Article That Does Not Exist"

    with pytest.raises(exceptions.ArticleNotFound):
        services.edit_article(article_to_edit, fields_to_change, uow)
