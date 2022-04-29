import model
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
