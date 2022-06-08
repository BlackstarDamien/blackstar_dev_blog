from abc import abstractmethod, ABC
from domain.model import Article
from typing import List, Optional


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, article: Article):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference: str):
        raise NotImplementedError

    @abstractmethod
    def list_items(self):
        raise NotImplementedError

    @abstractmethod
    def remove(self, reference: str):
        raise NotImplementedError

    @abstractmethod
    def next_reference(self, *args) -> str:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, article: Article):
        self.session.add(article)

    def get(self, reference: str) -> Article:
        result = self.session.query(Article).filter_by(reference=reference).one()
        return result

    def list_items(self) -> List[Article]:
        return self.session.query(Article).all()

    def remove(self, reference: str):
        article_to_remove = self.session.query(Article).filter_by(reference=reference).one()
        self.session.delete(article_to_remove)

    def next_reference(self, article_title: str, chars_limit: Optional[int]=None) -> str:
        chars_limit = chars_limit if chars_limit else len(article_title)
        slug_title = article_title.lower()
        slug_title = slug_title.replace(" ", "-")
        return f"{slug_title[:chars_limit]}"
