from datetime import date

import adapters.repository as repository
import domain.model as model


def test_repository_can_save_an_article_with_tags(session):
    """Tests that repository is able to save given article.
    """
    tags = {model.Tag("CI"), model.Tag("Jenkins")}
    article = model.Article(
        "test_id",
        "Importance of using CI/CD",
        "Tom Smith",
        date(2022, 4, 15),
        "Interesting stuff about CI/CD",
        "Something Something",
        tags,
    )
    repo = repository.SQLAlchemyRepository(session)
    repo.add(article)
    session.commit()

    result = list(
        session.execute(
            "SELECT reference, title, author, publication_date, description, content, t._name FROM articles a"
            " LEFT JOIN tags t on a.id = t.articles_id ORDER BY t._name;"
        )
    )
    sorted_tags = sorted(list([tag.name for tag in tags]))
    assert result == [
        (
            "test_id",
            "Importance of using CI/CD",
            "Tom Smith",
            "2022-04-15",
            "Interesting stuff about CI/CD",
            "Something Something",
            sorted_tags[0],
        ),
        (
            "test_id",
            "Importance of using CI/CD",
            "Tom Smith",
            "2022-04-15",
            "Interesting stuff about CI/CD",
            "Something Something",
            sorted_tags[1],
        ),
    ]

def test_repository_can_retreive_an_article(session):
    """Tests that repository is able to fetch article
    for given identifier.
    """
    session.execute(
        "INSERT INTO articles(reference, title, author, publication_date, description, content) VALUES "
        '("async-libs-in-python", "Async Libraries in Python", "Tom Smith", "2022-01-01", "Some async libs", "Lorem ipsum...");'
    )
    session.execute(
        "INSERT INTO tags(_name, articles_id) VALUES ('Async', 1), ('Python', 1);"
    )
    session.commit()

    repo = repository.SQLAlchemyRepository(session)
    article = repo.get("async-libs-in-python")

    assert article.reference == "async-libs-in-python"
    assert article.title == "Async Libraries in Python"
    assert article.author == "Tom Smith"
    assert article.publication_date == date(2022, 1, 1)
    assert article.description == "Some async libs"
    assert article.content == "Lorem ipsum..."
    assert article.tags == {model.Tag("Async"), model.Tag("Python")}

def test_should_generate_slug_reference_from_title(session):
    """Tests that repository is able to generate slug
    from given article's title.
    """
    repo = repository.SQLAlchemyRepository(session)
    title = "Asynchronous programming in Python"
    result = repo.next_reference(title)
    expected_slug = "asynchronous-programming-in-python"

    assert result == expected_slug

def test_should_shorten_slug_reference_to_given_chars_limit(session):
    """Tests that repository is able to generate slug
    for give title that is not longer than provided length.
    """
    repo = repository.SQLAlchemyRepository(session)
    title = "Importance of adding end to end tests in your microservice project"
    chars_limit = 20
    expected_slug = "importance-of-adding"
    result = repo.next_reference(title, chars_limit)

    assert result == expected_slug
