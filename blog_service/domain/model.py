from datetime import datetime
from typing import Optional, Set


class TagNameTooLong(Exception):
    pass


class EmptyTagName(Exception):
    pass


TAG_MAX_CHARS = 30


class Tag:
    """This value object represents tag assigned to article.
    Tag is used to create category used to filtering articles on blog.
    """
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
    """This entity represents article, that blog consists of.
    Each Article entity has it's title, author, content
    and other properties that can be used to identify given object.
    Also, to make identifying easy, every Article has it's own reference.
    This can be an url slug, uuid or any other thing that can be used
    as an identifier.
    """
    def __init__(
        self,
        reference: str,
        title: str,
        author: str,
        publication_date: datetime,
        description: str,
        content: str,
        tags: Optional[Set[Tag]] = set(),
    ):
        self.reference = reference
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.tags = tags
        self.description = description
        self.content = content

    def __hash__(self) -> int:
        return hash(self.reference)

    def __eq__(self, other) -> bool:
        return self.reference == other.reference
