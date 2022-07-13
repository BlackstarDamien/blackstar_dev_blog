import os


def get_api_url():
    host = os.getenv("API_HOST", "localhost")
    port = 5005 if host == "127.0.0.1" else 80
    url = f"http://{host}:{port}"
    return url


def get_postgres_uri():
    host = os.getenv("DB_HOST", "172.17.0.1")
    port = os.getenv("DB_PORT", 5432)
    password = os.getenv("DB_PASSWORD", "test123")
    user = "blog_user"
    db_name = "blog_db"
    uri = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    return uri
