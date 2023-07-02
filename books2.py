import datetime

from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status

from models2 import Book, BookModel

app = FastAPI()


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2020),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2002),
    Book(3, 'Master Endpoints', 'codingwithroby', 'An awesome book!', 5, 2019),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2018),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2017),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2016)
]


@app.get('/books', status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')


@app.get('/books/', status_code=status.HTTP_200_OK)
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = [book for book in BOOKS if book.rating == book_rating]
    return books_to_return


@app.get('/books/publish/', status_code=status.HTTP_200_OK)
async def get_book_by_publish(published_date: int = Query(gt=1000, lt=datetime.date.today().year)):
    books_to_return = [book for book in BOOKS if book.published_date == published_date]
    return books_to_return


@app.post('/create-book', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookModel):
    new_book = Book(**book_request.dict())
    BOOKS.append(get_book_id(new_book))


def get_book_id(book: Book):
    book.id = BOOKS[-1].id + 1 if BOOKS else 1
    return book


@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookModel):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')
