from abc import abstractmethod, ABC
from domain.model import Article


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, article: Article):
        raise NotImplementedError

    @abstractmethod
    def get(self, title: str):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, article: Article):
        self.session.add(article)

    def get(self, title: str) -> Article:
        result = self.session.query(Article).filter_by(title=title).one()
        return result
