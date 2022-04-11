from datetime import datetime
from typing import List


class Article:
    def __init__(
        self,
        title: str,
        author: str,
        publication_date: datetime,
        tags: List[str],
        description: str,
        content: str,
    ):
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.tags = tags
        self.description = description
        self.content = content
