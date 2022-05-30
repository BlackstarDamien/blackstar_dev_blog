from service_layer.helpers.slug_maker import create_slug

def test_should_generate_slug_from_title():
    title = "Asynchronous programming in Python"
    result = create_slug(title)
    expected_slug = "asynchronous-programming-in-python"

    assert result == expected_slug

def test_should_shorten_slug_to_given_chars_limit():
    title = "Importance of adding end to end tests in your microservice project"
    chars_limit = 20
    expected_slug = "importance-of-adding"
    result = create_slug(title, chars_limit)

    assert result == expected_slug
