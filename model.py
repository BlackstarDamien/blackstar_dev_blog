from datetime import datetime
from typing import List


class Article:
    def __init__(
        self,
        author: str,
        publication_date: datetime,
        tags: List[str],
        description: str,
        content: str,
    ):
        self._author = author
        self._publication_date = publication_date
        self._tags = tags
        self._description = description
        self._content = content

    def get_author(self) -> str:
        return self._author

    def get_publication_date(self) -> datetime:
        return self._publication_date

    def get_tags(self) -> List[str]:
        return self._tags

    def get_description(self) -> str:
        return self._description

    def read(self) -> str:
        return self._content
