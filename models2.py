from typing import Optional
import datetime

from pydantic import BaseModel, Field


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookModel(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1000, lt=datetime.date.today().year)

    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'A new author',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date': 2023
            }
        }

