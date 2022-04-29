from abc import abstractmethod, ABC
from model import Article


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, article: Article):
        raise NotImplementedError

    @abstractmethod
    def get(self, title: str):
        raise NotImplementedError
