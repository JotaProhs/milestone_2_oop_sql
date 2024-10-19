from .database_connection import DatabaseConnection
import sqlite3


class Book:
    book_schema = dict[str, str | int]
    database_file = 'data.db'

    def __init__(self, name: str, author: str):
        self.name = name
        self.author = author
        self.read = 0

    @classmethod
    def create_book_table(cls) -> None:
        with DatabaseConnection(cls.database_file) as (connection, cursor):
            cursor.execute('CREATE TABLE IF NOT EXISTS books (name TEXT '
                           'PRIMARY KEY, author TEXT, read INTEGER)')

    def add_book(self) -> bool:
        with DatabaseConnection(Book.database_file) as (connection, cursor):
            try:
                cursor.execute('INSERT INTO books VALUES(?, ?, ?)',
                               (self.name, self.author, self.read))
            except sqlite3.IntegrityError:
                return False
            else:
                return True

    @classmethod
    def get_all_books(cls) -> list[dict[str, str | int]]:
        with DatabaseConnection(cls.database_file) as (connection, cursor):
            cursor.execute('SELECT * FROM books')
            books = [
                {'name': row[0], 'author': row[1], 'read': row[2]}
                for row in cursor.fetchall()
            ]
        return books

    @classmethod
    def mark_book_read(cls, name: str) -> None:
        with DatabaseConnection(cls.database_file) as (connection, cursor):
            cursor.execute('UPDATE books SET read=1 WHERE name=?'
                           'COLLATE NOCASE', (name,))

    @classmethod
    def delete_book(cls, name) -> None:
        with DatabaseConnection(cls.database_file) as (connection, cursor):
            cursor.execute('DELETE FROM books WHERE name=? COLLATE NOCASE',
                           (name,))


if __name__ == '__main__':
    book = Book(name='Python Crash Course', author='Eric Matthes')
    book.get_all_books()
    book.mark_book_read()
    book.get_all_books()
    book.delete_book()
    book.get_all_books()