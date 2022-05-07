from datetime import datetime
from typing import Optional, Set


class TagNameTooLong(Exception):
    pass


class EmptyTagName(Exception):
    pass


TAG_MAX_CHARS = 30


class Tag:
    def __init__(self, name: str):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if len(value) == 0:
            raise EmptyTagName("Tag name should not be empty.")

        if len(value) > TAG_MAX_CHARS:
            raise TagNameTooLong(
                f"Provided name exceeded max length of {TAG_MAX_CHARS} characters."
            )

        self._name = value

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other) -> bool:
        return self.name == other.name


class Article:
    def __init__(
        self,
        title: str,
        author: str,
        publication_date: datetime,
        description: str,
        content: str,
        tags: Optional[Set[Tag]] = set(),
    ):
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.tags = tags
        self.description = description
        self.content = content

    def __hash__(self) -> int:
        return hash(self.title)

    def __eq__(self, other) -> bool:
        return self.title == other.title