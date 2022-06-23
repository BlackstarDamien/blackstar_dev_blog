from blog_service.service_layer import unit_of_work


def test_uow_can_fetch_article(session_factory):
    """Tests that unit of work is able to fetch article by
    given reference.
    """
    session = session_factory()
    insert_article(
        session,
        "test-article",
        "Test Article",
        "Kukulek",
        "2022-01-01",
        "Some cool article",
        "Something Something",
    )
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        article = uow.articles.get("test-article")

    assert article.reference == "test-article"


def insert_article(
    session, ref: str, title: str, author: str, date: str, desc: str, content: str
):
    session.execute(
        "INSERT INTO articles(reference, title, author, publication_date, description, content) VALUES "
        "(:ref, :title, :author, :date, :desc, :content);",
        dict(
            ref=ref, title=title, author=author, date=date, desc=desc, content=content
        ),
    )
