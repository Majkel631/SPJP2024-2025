from .database_manager import get_connection
from .models import Author, Book

def add_author(first_name, last_name, birth_year, nationality):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO authors (first_name, last_name, birth_year, nationality)
                      VALUES (?, ?, ?, ?)""", (first_name, last_name, birth_year, nationality))
    conn.commit()
    conn.close()

def get_all_authors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors")
    rows = cursor.fetchall()
    conn.close()
    return [Author(*row) for row in rows]

def find_author_by_last_name(last_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors WHERE last_name LIKE ?", (f"%{last_name}%",))
    authors = cursor.fetchall()
    conn.close()
    return [Author(*a) for a in authors]

def update_author(author_id, first_name, last_name, birth_year, nationality):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE authors SET first_name=?, last_name=?, birth_year=?, nationality=?
                      WHERE id=?""", (first_name, last_name, birth_year, nationality, author_id))
    conn.commit()
    conn.close()

def delete_author(author_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books WHERE author_id=?", (author_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("DELETE FROM authors WHERE id=?", (author_id,))
        conn.commit()
    conn.close()

def add_book(title, author_id, publication_year, genre, pages, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO books (title, author_id, publication_year, genre, pages, description)
                      VALUES (?, ?, ?, ?, ?, ?)""", (title, author_id, publication_year, genre, pages, description))
    conn.commit()
    conn.close()

def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return [Book(*b) for b in books]

def find_books_by_title_or_author_or_year(search_term):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT b.* FROM books b
                      JOIN authors a ON b.author_id = a.id
                      WHERE b.title LIKE ? OR a.last_name LIKE ? OR b.publication_year LIKE ?""",
                   (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    books = cursor.fetchall()
    conn.close()
    return [Book(*b) for b in books]

def update_book(book_id, title, author_id, publication_year, genre, pages, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE books SET title=?, author_id=?, publication_year=?, genre=?, pages=?, description=?
                      WHERE id=?""", (title, author_id, publication_year, genre, pages, description, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

def get_books_by_author(author_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE author_id=?", (author_id,))
    books = cursor.fetchall()
    conn.close()
    return [Book(*b) for b in books]

def stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    book_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM authors")
    author_count = cursor.fetchone()[0]
    cursor.execute("SELECT title FROM books ORDER BY publication_year ASC LIMIT 1")
    oldest = cursor.fetchone()
    cursor.execute("SELECT title FROM books ORDER BY publication_year DESC LIMIT 1")
    newest = cursor.fetchone()
    cursor.execute("""SELECT a.first_name || ' ' || a.last_name, COUNT(b.id) as count
                      FROM authors a JOIN books b ON a.id = b.author_id
                      GROUP BY a.id ORDER BY count DESC LIMIT 1""")
    top_author = cursor.fetchone()
    conn.close()
    return {
        "book_count": book_count,
        "author_count": author_count,
        "oldest": oldest[0] if oldest else "Brak",
        "newest": newest[0] if newest else "Brak",
        "top_author": top_author[0] if top_author else "Brak"
    }
