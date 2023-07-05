import datetime

from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status

from models2 import BookModel

app = FastAPI()


BOOKS = [
    BookModel(id=1, title='Computer Science Pro', author='codingwithroby', description='A very nice book!', rating=5, published_date=2020),
    BookModel(id=2, title='Be Fast with FastAPI', author='codingwithroby', description='A great book!', rating=5, published_date=2002),
    BookModel(id=3, title='Master Endpoints', author='codingwithroby', description='An awesome book!', rating=5, published_date=2019),
    BookModel(id=4, title='HP1', author='Author 1', description='Book Description', rating=2, published_date=2018),
    BookModel(id=5, title='HP2', author='Author 2', description='Book Description', rating=3, published_date=2017),
    BookModel(id=6, title='HP3', author='Author 3', description='Book Description', rating=1, published_date=2016)
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