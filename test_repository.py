import domain.model as model
import repository
from datetime import date


def test_repository_can_save_an_article_without_tags(session):
    article = model.Article(
        "Importance of using CI/CD",
        "Tom Smith",
        date(2022, 4, 15),
        "Interesting stuff about CI/CD",
        "Something Something",
    )
    repo = repository.SQLAlchemyRepository(session)
    repo.add(article)
    session.commit()

    result = list(
        session.execute(
            "SELECT title, author, publication_date, description, content FROM articles;"
        )
    )

    assert result == [
        (
            "Importance of using CI/CD",
            "Tom Smith",
            "2022-04-15",
            "Interesting stuff about CI/CD",
            "Something Something",
        )
    ]


def test_repository_can_save_an_article_with_tags(session):
    tags = {model.Tag("CI"), model.Tag("Jenkins")}
    article = model.Article(
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
            "SELECT title, author, publication_date, description, content, t._name FROM articles a"
            " LEFT JOIN tags t on a.id = t.articles_id ORDER BY t._name;"
        )
    )
    sorted_tags = sorted(list([tag.name for tag in tags]))
    assert result == [
        (
            "Importance of using CI/CD",
            "Tom Smith",
            "2022-04-15",
            "Interesting stuff about CI/CD",
            "Something Something",
            sorted_tags[0],
        ),
        (
            "Importance of using CI/CD",
            "Tom Smith",
            "2022-04-15",
            "Interesting stuff about CI/CD",
            "Something Something",
            sorted_tags[1],
        ),
    ]


def test_repository_can_retreive_an_article_without_tags(session):
    session.execute(
        "INSERT INTO articles(title, author, publication_date, description, content) VALUES "
        '("Async Libraries in Python", "Tom Smith", "2022-01-01", "Some async libs", "Lorem ipsum...");'
    )
    session.commit()

    repo = repository.SQLAlchemyRepository(session)
    article = repo.get("Async Libraries in Python")

    assert article.title == "Async Libraries in Python"
    assert article.author == "Tom Smith"
    assert article.publication_date == date(2022, 1, 1)
    assert article.description == "Some async libs"
    assert article.content == "Lorem ipsum..."


def test_repository_can_retreive_an_article_with_tags(session):
    session.execute(
        "INSERT INTO articles(title, author, publication_date, description, content) VALUES "
        '("Async Libraries in Python", "Tom Smith", "2022-01-01", "Some async libs", "Lorem ipsum...");'
    )
    session.execute(
        "INSERT INTO tags(_name, articles_id) VALUES ('Async', 1), ('Python', 1);"
    )
    session.commit()

    repo = repository.SQLAlchemyRepository(session)
    article = repo.get("Async Libraries in Python")

    assert article.title == "Async Libraries in Python"
    assert article.author == "Tom Smith"
    assert article.publication_date == date(2022, 1, 1)
    assert article.description == "Some async libs"
    assert article.content == "Lorem ipsum..."
    assert article.tags == {model.Tag("Async"), model.Tag("Python")}
