import uuid
from typing import Optional

def create_slug(title: str, chars_limit: Optional[int]=None) -> str:
    chars_limit = chars_limit if chars_limit else len(title)
    slug_title = title.lower()
    slug_title = slug_title.replace(" ", "-")
    return f"{slug_title[:chars_limit]}"
