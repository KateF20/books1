from fastapi import FastAPI, Body

app = FastAPI()


BOOKS = [
    {'title': 'Harry Potter One', 'author': 'J.K. Rowling', 'category': 'fantasy'},
    {'title': 'Harry Potter Two', 'author': 'J.K. Rowling', 'category': 'fantasy'},
    {'title': 'LOTR', 'author': 'J.R.R. Tolkien', 'category': 'fantasy'},
    {'title': 'Little Mermaid', 'author': 'H.Ch. Andersen', 'category': 'fairy tale'},
    {'title': 'War & Peace', 'author': 'L. Tolstoy', 'category': 'fiction'},
    {'title': 'Faust', 'author': 'W. von Goethe', 'category': 'fiction'}
]


@app.get("/books")
async def get_all_books():
    return BOOKS


@app.get('/books/')
async def get_book_by_category(category: str):
    books_to_return = [book for book in BOOKS if book.get('category').casefold() == category.casefold()]
    return books_to_return


@app.get('/books/author/')
async def get_book_by_author_query(author: str):
    books_to_return = [book for book in BOOKS if author.casefold() in book.get('author').casefold()]
    return books_to_return


@app.get('/books/author/{author}')
async def get_book_by_author_path(author: str):
    books_to_return = [book for book in BOOKS if author.casefold() in book.get('author').casefold()]
    return books_to_return


@app.get('/books/title/{book_title}')
async def get_book_by_title(book_title: str):
    books_to_return = [book for book in BOOKS if book_title.casefold() in book.get('title').casefold()]
    return books_to_return


@app.get("/books/{book_author}/")
async def get_author_category_by_query(book_author: str, category: str):
    books_to_return = [book for book in BOOKS if book.get('category').casefold() == category.casefold()
                       and book_author.casefold() in book.get('author').casefold()]
    return books_to_return


@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put('/books/update_book')
async def update_book_category(updated_book=Body()):
    for i in range(len(BOOKS)):
        if updated_book.get('title').casefold() in BOOKS[i].get('title').casefold():
            BOOKS[i] = updated_book


@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if book_title.casefold() in BOOKS[i].get('title').casefold():
            BOOKS.pop(i)
            break