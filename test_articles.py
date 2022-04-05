from model import Article

from datetime import datetime


def make_test_article(
    author="Noname",
    publication_date=datetime.now(),
    tags=[],
    description="",
    content="",
):
    article = Article(
        author=author,
        publication_date=publication_date,
        tags=tags,
        description=description,
        content=content,
    )

    return article


def test_can_see_who_is_the_author_of_the_article():
    expected_author = "Tom Smith"
    article = make_test_article(expected_author)
    articles_author = article.get_author()

    assert articles_author == expected_author


def test_can_see_when_article_was_published():
    expected_publication_date = datetime(2021, 1, 1)
    article = make_test_article(publication_date=expected_publication_date)
    articles_publication_date = article.get_publication_date()

    assert articles_publication_date == expected_publication_date


def test_can_see_attached_tags():
    expected_tags = ["javascript", "asynchronous programming", "mongo db"]
    article = make_test_article(tags=expected_tags)
    articles_tags = article.get_tags()

    assert articles_tags == expected_tags


def test_can_see_articles_description():
    expected_description = "Just some short article about nothing"
    article = make_test_article(description=expected_description)
    articles_description = article.get_description()

    assert articles_description == expected_description


def test_can_read_articles_content():
    expected_content = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt 
    mollit anim id est laborum.
    """
    article = make_test_article(content=expected_content)
    articles_content = article.read()

    assert articles_content == expected_content
