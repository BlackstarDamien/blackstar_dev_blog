import blog_service.adapters.repository as repository


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
