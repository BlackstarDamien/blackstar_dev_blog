from datetime import datetime
from typing import List


class TagNameTooLong(Exception):
    pass


class EmptyTagName(Exception):
    pass


class Tag:
    def __init__(self, name: str):
        self.name = name

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value: str):
        if len(value) == 0:
            raise EmptyTagName("Tag name should not be empty.")

        if len(value) > 20:
            raise TagNameTooLong("Provided name exceeded max length of 20 characters.")

        self.name = value


class Article:
    def __init__(
        self,
        title: str,
        author: str,
        publication_date: datetime,
        tags: List[Tag],
        description: str,
        content: str,
    ):
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.tags = tags
        self.description = description
        self.content = content
