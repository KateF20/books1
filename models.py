from typing import Optional
import datetime

from pydantic import BaseModel, Field


class BookModel(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1000, lt=datetime.date.today().year)

    def __init__(self, id, title, author, description, rating, published_date):
        super().__init__(id=id, title=title, author=author, description=description, rating=rating,
                         published_date=published_date)

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
