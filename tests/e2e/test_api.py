from datetime import date
from typing import List, Optional

import pytest
import requests

from src.blog_service.config import get_api_url


def post_to_add_article(title: str, author: str, publication_date: date,
                        description:str, content: str, tags: Optional[List[str]] = []):
    """Sends POST request into API to create new article described
    by provided arguments.

    Parameters
    ----------
    title : str
        Article's title.
    author : str
        Article's author.
    publication_date : date
        When an article was published.
    description : str
        Briefly described what article is about.
    content : str
        Actual content of an article/
    tags : Optional[List[str]], optional
        List of tags assigned to an article, by default []
    """
    url = get_api_url()
    article_to_add = {
        "title": title,
        "author": author,
        "publication_date": publication_date,
        "description": description,
        "content": content,
        "tags": tags
    }
    response = requests.post(f"{url}/articles", json=article_to_add)

    assert response.status_code == 201

@pytest.mark.usefixtures("postgres_session")
def test_get_articles_endpoint_returns_200_and_all_articles():
    """Tests that API is able to list all available articles.
    """
    post_to_add_article("Async Libraries in Python", "Tom Smith", "2022-01-01", "Some async libs", "Lorem ipsum...")
    post_to_add_article("Why Docker is the best", "Carl Johnson", "2016-05-09", "Why Docker is cool", "Docker is cool", ["Docker", "Infrastructure"])
    post_to_add_article("PHP - A language of the internet", "John Doe", "2018-10-12", "About PHP", "Lorem ipsum..")

    api_url = get_api_url()
    articles = requests.get(f"{api_url}/articles")

    assert articles.status_code == 200
    assert len(articles.json()["articles"]) == 3

@pytest.mark.usefixtures("postgres_session")
def test_get_article_endpoint_returns_200_and_specified_article():
    """Tests that API is able to provide article for given title.
    """
    post_to_add_article("Async Libraries in Python", "Tom Smith", "2022-01-01", "Some async libs", "Lorem ipsum...")
    searched_title = "Async Libraries in Python"
    api_url = get_api_url()
    article = requests.get(f"{api_url}/articles/async-libraries-in-python")

    assert article.status_code == 200
    assert article.json()["title"] == searched_title

@pytest.mark.usefixtures("postgres_session")
def test_get_article_endpoint_returns_404_and_specified_article():
    """Tests that API is able to send error message when article
    is not found.
    """
    api_url = get_api_url()
    article = requests.get(f"{api_url}/articles/article-that-does-not-exist")

    assert article.status_code == 404
    assert article.json()["message"] == f"Article not found."

@pytest.mark.usefixtures("postgres_session")
def test_post_article_should_return_400_and_error_message():
    """Tests that API returns error message when article meant to create
    already exists.
    """
    with open("./tests/test_data/example_article.txt") as f:
        article_content = f.read()

    post_to_add_article("Custom hooks in React",
                        "Tommy Vercetti" , "2022-12-05",
                        "Let's see how you can easily create your own hooks in React",
                        article_content, ["Hooks", "React", "Javascript"])

    article_to_add = {
        "title": "Custom hooks in React",
        "author": "Tommy Vercetti",
        "publication_date": "2022-12-05",
        "description": "Let's see how you can easily create your own hooks in React",
        "content": article_content,
        "tags": ["Hooks", "React", "Javascript"],
    }

    api_url = get_api_url()
    post_request = requests.post(f"{api_url}/articles", json=article_to_add)

    assert post_request.status_code == 400
    assert post_request.json()["message"] == f"Article already exists."

@pytest.mark.usefixtures("postgres_session")
def test_patch_article_should_return_200_and_success_message():
    """Tests that API is able to edit existing article with new values
    of it's own properties.
    """
    post_to_add_article("Async Libraries in Python", "Tom Smith", "2022-01-01", "Some async libs", "Lorem ipsum...", ["Async", "Programming"])
    fields_to_change = {
        "content": "Some new fresh content",
        "description": "Some new description",
        "tags": ["Python", "Coding"]
    }

    api_url = get_api_url()
    patch_request = requests.patch(f"{api_url}/articles/async-libraries-in-python", json=fields_to_change)

    assert patch_request.status_code == 200
    assert patch_request.json()["message"] == "Article successfully edited."

@pytest.mark.usefixtures("postgres_session")
def test_patch_articles_should_return_400_and_error_message():
    """Tests that API returns error message when trying to
    edit nonexistent article.
    """
    fields_to_change = {
        "content": "Some new fresh content",
        "description": "Some new description",
        "tags": ["Python", "Coding"]
    }

    api_url = get_api_url()
    patch_request = requests.patch(f"{api_url}/articles/async-libraries-in-python", json=fields_to_change)

    assert patch_request.status_code == 404
    assert patch_request.json()["message"] == "Article not found."

@pytest.mark.usefixtures("postgres_session")
def test_delete_article_should_return_200_and_success_message():
    """Tests that API can remove existig article.
    """
    post_to_add_article("Async Libraries in Python", "Tom Smith", "2022-01-01", "Some async libs", "Lorem ipsum...")

    api_url = get_api_url()
    delete_request = requests.delete(f"{api_url}/articles/async-libraries-in-python")

    assert delete_request.status_code == 200
    assert delete_request.json()["message"] == "Article successfully removed."

@pytest.mark.usefixtures("postgres_session")
def test_delete_article_should_return_400_and_error_message():
    """Tests that API throws error message when article
    meant to remove does not exist.
    """
    api_url = get_api_url()
    delete_request = requests.delete(f"{api_url}/articles/async-libraries-in-python")

    assert delete_request.status_code == 404
    assert delete_request.json()["message"] == "Article not found."
