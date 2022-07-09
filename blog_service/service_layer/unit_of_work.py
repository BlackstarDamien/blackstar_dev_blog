from abc import ABC, abstractmethod

from blog_service import config
from blog_service.adapters.repository import (AbstractRepository,
                                              SQLAlchemyRepository)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AbstractUnitOfWork(ABC):
    articles: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(config.get_postgres_uri(), pool_pre_ping=True)
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        """Initialize session and instatiate repository
        to prepare unit of work for executing atomic operation
        on database layer.
        """
        self.session = self.session_factory()
        self.articles = SQLAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        """When operation finished with success or failed,
        it rollback changes made during the session
        and close session object.
        """
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        """Approves changes made during the session.
        """
        self.session.commit()

    def rollback(self):
        """Revert all changes made during the session.
        """
        self.session.rollback()
