from datetime import datetime

import pytest

from src.blog_service.domain.model import Article, EmptyTagName, Tag, TagNameTooLong


def test_can_initialize_an_article_object_without_tags():
    """Tests that an Article entity can be instantiated without tags."""
    expected_ref = "test_id"
    expected_title = "Javascript for Dummies"
    expected_author = "Tom Smith"
    expected_publication_date = datetime(2021, 1, 1)
    expected_description = "Just some short article about nothing"
    expected_content = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
    mollit anim id est laborum.
    """

    article = Article(
        reference=expected_ref,
        title=expected_title,
        author=expected_author,
        publication_date=expected_publication_date,
        description=expected_description,
        content=expected_content,
    )

    assert article.reference == expected_ref
    assert article.title == expected_title
    assert article.author == expected_author
    assert article.publication_date == expected_publication_date
    assert article.description == expected_description
    assert article.content == expected_content


def test_can_initialize_an_article_object_with_tags():
    """Tests that an Article entity can be instantiated with tags."""
    expected_ref = "test_id"
    expected_title = "Javascript for Dummies"
    expected_author = "Tom Smith"
    expected_publication_date = datetime(2021, 1, 1)
    expected_tags = {
        Tag("javascript"),
        Tag("asynchronous programming"),
        Tag("mongo db"),
    }
    expected_description = "Just some short article about nothing"
    expected_content = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
    mollit anim id est laborum.
    """

    article = Article(
        reference=expected_ref,
        title=expected_title,
        author=expected_author,
        publication_date=expected_publication_date,
        tags=expected_tags,
        description=expected_description,
        content=expected_content,
    )

    assert article.tags == expected_tags


def test_tag_should_raise_exception_when_name_is_empty():
    """Tests that a Tag value object raises exception when
    provided name is empty."""
    with pytest.raises(EmptyTagName):
        Tag("")


def test_tag_shoul_raise_exception_when_name_is_too_long():
    """Tests that a Tag value object raises exception when
    provided name is too long.
    """
    with pytest.raises(TagNameTooLong):
        Tag("Lorem ipsum dolor sit amet, consectetur adipiscing elit")
