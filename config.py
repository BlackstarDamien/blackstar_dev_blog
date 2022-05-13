import os


def get_api_url():
    host = os.getenv("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    url = f"http://{host}:{port}"
    return url


def get_postgres_uri():
    host = os.getenv("DB_HOST", "localhost")
    port = 54321 if host == "localhost" else 5432
    password = os.getenv("DB_PASSWORD", "test123")
    user = "blog_user"
    db_name = "articles"
    uri = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    return uri
