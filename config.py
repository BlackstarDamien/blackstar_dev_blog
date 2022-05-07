import os


def get_api_url():
    host = os.getenv("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    url = f"http://{host}:{port}"
    return url
