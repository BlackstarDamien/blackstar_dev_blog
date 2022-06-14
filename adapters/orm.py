from sqlalchemy import (Column, Date, ForeignKey, Integer, MetaData, String,
                        Table, Text)
from sqlalchemy.orm import mapper, relationship

import domain.model as model

metadata = MetaData()


articles = Table(
    "articles",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("title", String(255), nullable=False),
    Column("author", String(255), nullable=False),
    Column("publication_date", Date),
    Column("description", Text),
    Column("content", Text),
)

tags = Table(
    "tags",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("_name", String(model.TAG_MAX_CHARS), nullable=False),
    Column("articles_id", ForeignKey("articles.id")),
)


def start_mappers():
    """Gets Table objects and map them with proper domain models."""
    tags_mapper = mapper(
        model.Tag,
        tags,
    )
    mapper(
        model.Article,
        articles,
        properties={
            "tags": relationship(
                tags_mapper, uselist=True, collection_class=set, backref="articles",
                cascade="all, delete, delete-orphan"
            ),
        },
    )
