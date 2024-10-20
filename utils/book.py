from .database_connection import DatabaseConnection
import sqlite3


class Book:
    """
    A class representing a book.
    """
    database_file = 'data.db'

    def __init__(self, name: str, author: str):
        """
        Every book is instantiated with 2 positional arguments {name, author).
        One default argument (read=0 (meaning the book is not read)
        :param name: provided by the user in the app.py.
        :param author: provided by the user in the app.py.
        """
        self.name = name
        self.author = author
        self.read = 0

    @classmethod
    def create_book_table(cls) -> None:
        """
        Context manager in charge of creating the SQL table with the columns:
        name, author and read. name is the primary column, and it is the one
        that does not accept duplicates.
        :return: None
        """
        with DatabaseConnection(cls.database_file) as (connection, cursor):
            cursor.execute('CREATE TABLE IF NOT EXISTS books (name TEXT '
                           'PRIMARY KEY, author TEXT, read INTEGER)')

    def add_book(self) -> bool:
        """
        Open DB and inserts a new book to the table. Manage the error if
        the entered book is already in the db.
        :return: True when executes with no errors, False when an error is
        raised (duplicate values)
        """
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
        """
        Iterates over all the books in the table books and fetch them all
        with a dict comprehension. Saves the dict comprehension and returns it.
        :return: List of dicts where each dict is a book.
        """
        with DatabaseConnection(cls.database_file) as (connection, cursor):
            cursor.execute('SELECT * FROM books')
            books = [
                {'name': row[0], 'author': row[1], 'read': row[2]}
                for row in cursor.fetchall()
            ]
        return books

    @classmethod
    def mark_book_read(cls, name: str) -> None:
        """
        Takes the book provided by the user as a parameter and updates it
        read value in the db.
        :param name: input provided by the user
        :return: None
        """
        with DatabaseConnection(cls.database_file) as (connection, cursor):
            cursor.execute('UPDATE books SET read=1 WHERE name=?'
                           'COLLATE NOCASE', (name,))

    @classmethod
    def delete_book(cls, name) -> None:
        """
        Takes name as an argument and deletes the book that matches that
        provided name.
        :param name: provided by the user in app.py
        :return: None.
        """
        with DatabaseConnection(cls.database_file) as (connection, cursor):
            cursor.execute('DELETE FROM books WHERE name=? COLLATE NOCASE',
                           (name,))


if __name__ == '__main__':
    book = Book(name='Python Crash Course', author='Eric Matthes')
