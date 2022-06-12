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
        """Adds article into repository

        Parameters
        ----------
        article : Article
            Article to add.
        """
        self.session.add(article)

    def get(self, reference: str) -> Article:
        """Fetch Article object by using it's identifier.

        Parameters
        ----------
        reference : str
            An Article's identifier

        Returns
        -------
        Article
            Fetched article.
        """
        result = self.session.query(Article).filter_by(reference=reference).one()
        return result

    def list_items(self) -> List[Article]:
        """Shows all available articles in repository.

        Returns
        -------
        List[Article]
            List of available articles.
        """
        return self.session.query(Article).all()

    def remove(self, reference: str):
        """Removes article referenced by provided identifier from repository.

        Parameters
        ----------
        reference : str
            An Article's identifier.
        """
        article_to_remove = self.session.query(Article).filter_by(reference=reference).one()
        self.session.delete(article_to_remove)

    def next_reference(self, article_title: str, chars_limit: Optional[int]=None) -> str:
        """Generates slug for given article's title with set limit of chars.
        That slug is used as an article's identifier in repository.

        Parameters
        ----------
        article_title : str
            Article's title that will be slugified.
        chars_limit : Optional[int], optional
            Lenght of generated slug, by default None.
            When None, it takes length of provided title.

        Returns
        -------
        str
            Generated slug.
        """
        chars_limit = chars_limit if chars_limit else len(article_title)
        slug_title = article_title.lower()
        slug_title = slug_title.replace(" ", "-")
        return f"{slug_title[:chars_limit]}"
