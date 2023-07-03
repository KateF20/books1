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
async def get_book_by_query(category: str = None, author: str = None, title: str = None):
    books_to_return = BOOKS
    if category:
        books_to_return = filter(lambda book: book['category'].casefold() == category.casefold(), books_to_return)
    if author:
        books_to_return = filter(lambda book: author.casefold() in book['author'].casefold(), books_to_return)
    if title:
        books_to_return = filter(lambda book: title.casefold() in book['title'].casefold(), books_to_return)

    return list(books_to_return)


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
