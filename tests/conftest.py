import pytest
from blog_service import config
from blog_service.adapters.orm import metadata, start_mappers
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker


def clean_db(session):
    session.execute("DELETE FROM tags;")
    session.execute("DELETE FROM articles;")
    session.execute("ALTER SEQUENCE articles_id_seq RESTART WITH 1;")
    session.execute("ALTER SEQUENCE tags_id_seq RESTART WITH 1;")
    session.commit()


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(session_factory):
    return session_factory()


@pytest.fixture
def postgres_db(scope="session"):
    engine = create_engine(config.get_postgres_uri())
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    start_mappers()
    session = sessionmaker(bind=postgres_db)()
    yield session
    clear_mappers()
    clean_db(session)
