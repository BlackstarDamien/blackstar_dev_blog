from model import Article
from datetime import date


def test_article_mapper_can_load_articles(session):
    session.execute(
        "INSERT INTO articles(title, author, publication_date, description, content) VALUES "
        '("Async Libraries in Python", "Tom Smith", "2022-01-01", "Some async libs", "Lorem ipsum...")'
        '("Why Docker is the best", "Carl Johnson", "2016-05-09, "Why Docker is cool", "Docker is cool")'
        '("PHP - A language of the internet", "John Doe", "2018-10-12", "About PHP", "Lorem ipsum..");'
    )
    expected = [
        Article(
            "Async Libraries in Python",
            "Tom Smith",
            date(2022, 1, 1),
            "Some async libs",
            "Lorem ipsum...",
        ),
        Article(
            "Why Docker is the best",
            "Carl Johnson",
            date(2016, 5, 9),
            "Why Docker is cool",
            "Docker is cool",
        ),
        Article(
            "PHP - A language of the internet",
            "John Doe",
            date(2018, 10, 12),
            "About PHP",
            "Lorem ipsum...",
        ),
    ]

    assert session.query(Article).all() == expected


def test_article_mapper_can_save_articles(session):
    new_article = Article(
        "PHP - A language of the internet",
        "John Doe",
        date(2018, 10, 12),
        "About PHP",
        "Lorem ipsum...",
    )
    session.add(new_article)
    session.commit()

    result = list(
        session.execute(
            "SELECT title, author, publication_date, description, content FROM articles;"
        )
    )

    # fmt: off
    assert result == [("PHP - A language of the internet", "John Doe",
                        date(2018, 10, 12), "About PHP", "Lorem ipsum...")]
    #fmt: onn
