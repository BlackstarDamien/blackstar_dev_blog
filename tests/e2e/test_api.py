from datetime import date
from config import get_api_url
import requests


def test_api_returns_all_articles():
    api_url = get_api_url()
    articles = requests.get(f"{api_url}/articles")

    assert articles.status_code == 200
    assert len(articles.json()["articles"]) == 5


def test_api_returns_specified_article():
    searched_title = "Async programming in Python"
    api_url = get_api_url()
    article = requests.get(f"{api_url}/article", json={"title": searched_title})

    assert article.status_code == 200
    assert article.json()["title"] == searched_title


def test_api_should_save_articles():
    with open("../test_data/example_article.txt") as f:
        article_content = f.read()

    article_to_add = {
        "title": "Custom hooks in React",
        "author": "Tommy Vercetti",
        "publication_date": date(2022, 5, 12),
        "description": "Let's see how you can easily create your own hooks in React",
        "content": article_content,
        "tags": {"Hooks", "React", "Javascript"},
    }

    api_url = get_api_url()
    post_request = requests.post(f"{api_url}/article", json=article_to_add)

    assert post_request.status_code == 201

    added_article = requests.get(
        f"{api_url}/article", json={"title": article_to_add["title"]}
    )
    added_article_json = added_article.json()

    assert added_article.status_code == 200
    assert added_article_json["title"] == article_to_add["title"]
    assert added_article_json["author"] == article_to_add["author"]
    assert added_article_json["publication_date"] == article_to_add["publication_date"]
    assert added_article_json["description"] == article_to_add["description"]
    assert added_article_json["content"] == article_to_add["content"]
    assert added_article_json["tags"] == article_to_add["tags"]
