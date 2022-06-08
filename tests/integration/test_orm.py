from domain.model import Article, Tag
from datetime import date


def test_article_mapper_can_load_articles(session):
    session.execute(
        "INSERT INTO articles(reference, title, author, publication_date, description, content) VALUES "
        '("ref1", "Async Libraries in Python", "Tom Smith", "2022-01-01", "Some async libs", "Lorem ipsum..."),'
        '("ref2", "Why Docker is the best", "Carl Johnson", "2016-05-09", "Why Docker is cool", "Docker is cool"),'
        '("ref3", "PHP - A language of the internet", "John Doe", "2018-10-12", "About PHP", "Lorem ipsum..");'
    )
    session.execute(
        "INSERT INTO tags(_name, articles_id) VALUES ('Docker', 2), ('Infrastructure', 2);"
    )
    expected = [
        Article(
            "ref1",
            "Async Libraries in Python",
            "Tom Smith",
            date(2022, 1, 1),
            "Some async libs",
            "Lorem ipsum...",
        ),
        Article(
            "ref2",
            "Why Docker is the best",
            "Carl Johnson",
            date(2016, 5, 9),
            "Why Docker is cool",
            "Docker is cool",
            {Tag("Docker"), Tag("Infrastructure")},
        ),
        Article(
            "ref3",
            "PHP - A language of the internet",
            "John Doe",
            date(2018, 10, 12),
            "About PHP",
            "Lorem ipsum...",
        ),
    ]

    assert session.query(Article).all() == expected


def test_article_mapper_can_save_articles(session):
    tags = {Tag("PHP"), Tag("Programming")}
    new_article = Article(
        "test_id",
        "PHP - A language of the internet",
        "John Doe",
        date(2018, 10, 12),
        "About PHP",
        "Lorem ipsum...",
        tags,
    )
    session.add(new_article)
    session.commit()

    result = list(
        session.execute(
            "SELECT reference, title, author, publication_date, description, content, t._name as tag FROM articles a\
            LEFT JOIN tags t on a.id = t.articles_id;",
        )
    )

    tags_sorted = sorted([tag.name for tag in tags])
    # fmt: off
    assert result == [("test_id", "PHP - A language of the internet", "John Doe",
                        "2018-10-12", "About PHP", "Lorem ipsum...", tags_sorted[0]),
                    ("test_id", "PHP - A language of the internet", "John Doe",
                        "2018-10-12", "About PHP", "Lorem ipsum...", tags_sorted[1])]
    # fmt: on
