from copy import deepcopy
from datetime import date

import pytest
from blog_service.domain.model import Article, Tag
from blog_service.service_layer import unit_of_work

TEST_DATA = {
    "reference": "test-article",
    "title": "Test Article",
    "author": "Kukulek",
    "publication_date": date(2022, 1, 1),
    "description": "Some cool article",
    "content": "Something Something",
    "tags": {"test1", "test2"},
}

ANOTHER_TEST_DATA = {
    "reference": "test-article2",
    "title": "Test Article Vol 2",
    "author": "Kukulek",
    "publication_date": date(2022, 5, 1),
    "description": "Some cool article again",
    "content": "Something Something Something",
}


def insert_article(session, data_to_insert: dict):
    session.execute(
        "INSERT INTO articles(reference, title, author, publication_date, description, content) VALUES "
        "(:reference, :title, :author, :publication_date, :description, :content);",
        data_to_insert,
    )

    if "tags" in data_to_insert:
        article_id = session.execute(
            "SELECT id FROM articles WHERE reference=:reference;",
            dict(reference=data_to_insert["reference"]),
        ).fetchone()[0]

        for tag in data_to_insert["tags"]:
            session.execute(
                "INSERT INTO tags(_name, articles_id) VALUES (:name, :articles_id);",
                dict(name=tag, articles_id=article_id),
            )


def test_uow_can_list_articles(session_factory):
    """Tests that unit of work is able to list all articles."""
    session = session_factory()
    insert_article(session, TEST_DATA)
    insert_article(session, ANOTHER_TEST_DATA)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        articles = deepcopy(uow.articles.list_items())

    assert len(articles) > 0


def test_uow_can_fetch_article(session_factory):
    """Tests that unit of work is able to fetch article by
    given reference.
    """
    session = session_factory()
    insert_article(session, TEST_DATA)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        article = deepcopy(uow.articles.get("test-article"))

    assert article.reference == "test-article"


def test_uow_can_save_article(session_factory):
    """Tests that unit of work is able to save article by
    given reference.
    """
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    test_article = deepcopy(TEST_DATA)
    test_article["tags"] = {Tag(name) for name in test_article["tags"]}

    with uow:
        article = Article(**test_article)
        uow.articles.add(article)
        uow.commit()

    new_session = session_factory()
    article = list(
        new_session.execute("SELECT * FROM articles WHERE reference='test-article';")
    )[0]
    assert article.reference == test_article["reference"]


def test_uow_can_remove_article(session_factory):
    """Tests that unit of work is able to remove article by
    given reference.
    """
    session = session_factory()
    insert_article(session, TEST_DATA)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        uow.articles.remove("test-article")
        uow.commit()

    new_session = session_factory()
    article = list(
        new_session.execute("SELECT * FROM articles WHERE reference='test-article';")
    )
    assert article == []


def test_rolls_back_uncommitted_work_by_default(session_factory):
    """Tests that unit of work reverts uncomitted changes in the session."""
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)

    with uow:
        insert_article(uow.session, TEST_DATA)
    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "articles"'))
    assert rows == []


def test_rolls_back_on_error(session_factory):
    """Tests that unit of work is able to revert changes
    when exception was thrown.
    """

    class TestException(Exception):
        pass

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(TestException):
        with uow:
            insert_article(uow.session, TEST_DATA)
        raise TestException

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "articles"'))
    assert rows == []
