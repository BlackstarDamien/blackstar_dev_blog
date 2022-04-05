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
        self.__author = author
        self.__publication_date = publication_date
        self.__tags = tags
        self.__description = description
        self.__content = content

    def who_wrote_it(self) -> str:
        return self.__author

    def when_was_published(self) -> datetime:
        return self.__publication_date

    def which_tags_it_has(self) -> List[str]:
        return self.__tags

    def what_is_about(self) -> str:
        return self.__description

    def read(self) -> str:
        return self.__content
