from entrypoints.helpers.slug_maker import create_slug


def test_should_create_slug_from_title_and_id():
    id = 1234
    title = "Asynchronous programming in Python"
    expected_slug = "asynchronous-programming-in-python-1234"
    result = create_slug(title, id)

    assert result == expected_slug

def test_should_shorten_slug_to_given_chars_limit():
    id = 4567
    title = "Importance of adding end to end tests in your microservice project"
    chars_limit = 20
    expected_slug = "importance-of-adding-4567"
    result = create_slug(title, id, chars_limit)

    assert result == expected_slug

def test_should_generate_slug_from_title_only():
    title = "Asynchronous programming in Python"
    result = create_slug(title)

    assert "asynchronous-programming-in-python" in result
