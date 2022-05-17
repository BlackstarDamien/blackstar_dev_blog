FROM python:3.10-slim-bullseye

RUN apt-get update
RUN apt install -y git gcc postgresql postgresql-client musl-dev python3-dev
RUN apt install -y libpq-dev

COPY requirements.txt /tmp
RUN pip install -r tmp/requirements.txt

RUN mkdir -p /code
COPY . /code/
WORKDIR /code

ENV FLASK_APP=entrypoints/api.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]
