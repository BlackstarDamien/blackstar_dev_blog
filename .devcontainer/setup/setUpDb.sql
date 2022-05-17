CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    publication_date DATE,
    description TEXT,
    content TEXT
);


CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY NOT NULL,
    _name VARCHAR NOT NULL,
    articles_id INT NOT NULL,
    FOREIGN KEY (articles_id)
      REFERENCES articles (id)
);
