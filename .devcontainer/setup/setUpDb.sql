DROP TABLE IF EXISTS articles CASCADE;
CREATE TABLE articles (
    id SERIAL PRIMARY KEY NOT NULL,
    reference VARCHAR,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    publication_date DATE,
    description TEXT,
    content TEXT
);

DROP TABLE IF EXISTS tags;
CREATE TABLE tags (
    id SERIAL PRIMARY KEY NOT NULL,
    _name VARCHAR NOT NULL,
    articles_id INT NOT NULL,
    FOREIGN KEY (articles_id)
      REFERENCES articles (id)
);
