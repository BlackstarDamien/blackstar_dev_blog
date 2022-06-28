from copy import deepcopy

import pytest
from blog_service.service_layer import unit_of_work

TEST_DATA = {
    "ref": "test-article",
    "title": "Test Article",
    "author": "Kukulek",
    "date": "2022-01-01",
    "desc": "Some cool article",
    "content": "Something Something",
}


def insert_article(session, data_to_insert: dict):
    session.execute(
        "INSERT INTO articles(reference, title, author, publication_date, description, content) VALUES "
        "(:ref, :title, :author, :date, :desc, :content);",
        data_to_insert,
    )


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
