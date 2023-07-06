import datetime

from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status

from models2 import BookModel

app = FastAPI()


BOOKS = [
    BookModel(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2020),
    BookModel(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2002),
    BookModel(3, 'Master Endpoints', 'codingwithroby', 'An awesome book!', 5, 2019),
    BookModel(4, 'HP1', 'Author 1', 'Book Description', 2, 2018),
    BookModel(5, 'HP2', 'Author 2', 'Book Description', 3, 2017),
    BookModel(6, 'HP3', 'Author 3', 'Book Description', 1, 2016)
]


@app.get('/books')
async def get_all_books():
    return BOOKS


@app.get('/books/{book_id}')
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')


@app.get('/books/')
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = [book for book in BOOKS if book.rating == book_rating]
    return books_to_return


@app.get('/books/publish/')
async def get_book_by_publish(published_date: int = Query(gt=1000, lt=datetime.date.today().year)):
    books_to_return = [book for book in BOOKS if book.published_date == published_date]
    return books_to_return


@app.post('/create-book', status_code=status.HTTP_201_CREATED)
async def create_book(book_model: BookModel):
    new_book = BookModel(**book_model.dict())
    BOOKS.append(get_book_id(new_book))


def get_book_id(book: BookModel):
    book.id = BOOKS[-1].id + 1 if BOOKS else 1
    return book


@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookModel):
    book_changed = False
    for i, current_book in enumerate(BOOKS):
        if current_book.id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i, current_book in enumerate(BOOKS):
        if current_book.id == book_id:
            del BOOKS[i]
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')
