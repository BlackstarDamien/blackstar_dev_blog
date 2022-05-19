import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from adapters.orm import metadata, start_mappers

import config


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture
def postgres_db(scope='session'):
    engine = create_engine(config.get_postgres_uri())
    metadata.create_all(engine)
    return engine

@pytest.fixture
def postgres_session(postgres_db):
    start_mappers()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()

@pytest.fixture
def add_articles(postgres_session):
    added_articles = set()

    def _add_articles(lines):
        for title, author, date, desc, content in lines:
            postgres_session.execute(
                'INSERT INTO articles (title, author, publication_date, description, content)'
                ' VALUES (:title, :author, :pub_date, :desc, :content);',
                dict(title=title, author=author, pub_date=date, desc=desc, content=content)
            )
            [[article_id]] = postgres_session.execute(
                "SELECT id FROM articles WHERE title=:title AND author=:author;",
                dict(title=title, author=author)
                )
            added_articles.add(article_id)

        postgres_session.commit()

    yield _add_articles

    for article_id in added_articles:
        postgres_session.execute(
            "DELETE FROM articles WHERE id=:article_id",
            dict(article_id=article_id)
        )

    postgres_session.execute(
            "ALTER SEQUENCE tags_id_seq RESTART WITH 1;"
        )
    postgres_session.commit()

@pytest.fixture
def add_tags_to_article(postgres_session):
    added_tags = set()

    def _add_tags(lines, title, author):
        [[article_id]] = postgres_session.execute(
                "SELECT id FROM articles WHERE title=:title AND author=:author;",
                dict(title=title, author=author)
                )

        for tag_name in lines:
            postgres_session.execute(
                'INSERT INTO tags (_name, articles_id)'
                ' VALUES (:name, :article_id);',
                dict(name=tag_name, article_id=article_id)
            )
            [[tag_id]] = postgres_session.execute(
                "SELECT id FROM tags WHERE _name=:name AND articles_id=:article_id;",
                dict(name=tag_name, article_id=article_id)
                )
            added_tags.add(tag_id)

        postgres_session.commit()

    yield _add_tags

    for tag_id in added_tags:
        postgres_session.execute(
            "DELETE FROM tags WHERE id=:tag_id;",
            dict(tag_id=tag_id)
        )

    postgres_session.execute(
            "ALTER SEQUENCE tags_id_seq RESTART WITH 1;"
        )

    postgres_session.commit()
