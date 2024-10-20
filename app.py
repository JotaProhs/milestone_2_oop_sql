from typing import Union
from utils.book import Book
import textwrap
import sys


class Menu:
    def __init__(self):
        """
        Initialize the meni with 2 attributes: menu_selection, a dictionary
        holding the options as keys and the call to the corresponding method
        as a value to the corresponding key. menu_options, the text displaying
        the options to the user.
        """
        self.menu_selection = {
            'a': self.prompt_add_book,
            'l': self.list_books,
            'r': self.prompt_read_book,
            'd': self.prompt_delete_book,
            'q': self.quit_program,
        }
        self.menu_prompt = textwrap.dedent("""
            - 'a' to add a new book.
            - 'l' to list all the books.
            - 'r' to mark a book as read.
            - 'd' to delete a book.
            - 'q' to quit
             """)

    def display_menu(self) -> None:
        """
        Display the menu options in the multiline string.
        :return: None
        """
        print(self.menu_prompt)

    def prompt_add_book(self) -> None:
        """
        Takes the name and author input from the useer, validates
        if the user has entered a valid value for both (no empty space).
        If the user has pressed enter without entering a value, lets the
        user know, and then ends the method by returning it. If there are
        values in name and author, the function continues by creating an
        object Book with the name and the author provided by the user.
        Finally calls the class Book method add_book and validates if it
        returns anything. Book.add_book returns True when the book is added
        with no error raised, and returns False when an error is raised. The
        error is checking for no duplicates.
        :return: None
        """
        name = input('Write the name of the book: -->  ').strip()
        author = input('Write the name of the author: -->  ').strip()
        if not name or not author:
            print('Both, book name and author are required.')
            return
        book = Book(name, author)
        if book.add_book():
            print(f"The book {name.title()} by {author.title()}"
                  f" has been added to your list.")
        else:
            print(f"The book {name.title()} by {author.title()}"
                  f" is already in the list. Duplicates not allowed.")

    def list_books(self) -> None:
        """
        variable books holds the list of dicts (books) returned by
        Book.get_all_books. If there are no books returned, lets the user
        know the list is empty. Otherwise, iterates over books and prints
        each book with enumerate starting at 1. Prints the name, author and
        if they have been read or not.
        :return: None
        """
        books: list[dict[str, str | int]] = Book.get_all_books()
        if not books:
            print('There are no books in your list yet.')
        else:
            for i, book in enumerate(books, start=1):
                read = ('Already read.' if book['read'] else 'Not read yet.')
                print(f"{i}. {book['name'].title()} by "
                      f"{book['author'].title()} - {read}")

    def prompt_read_book(self):
        """
        Saves the prompt that is going to be passed to _iterate method in the
        prompt variable.read_book holds the returned value of
        _iterate_over_books. read_book could be none if there are still no
        books, and it can also be the book itself in a dict format,
        where the key is a str and the values are a combination of sts and
        int. If _iterate returns a value (book), also validates if the book
        read value is 1, meaning it has already been read. If read = 1,
        lets the user know that this book had already been marked as read
        before. if book['read'] == 0, call the method Book.mark_book_read,
        which updates the book to be read and prints the confirmation message.
        :return: None
        """
        prompt = 'Write the name of the book you want to mark as read: -->  '
        read_book: Union[dict[str, str | int], None] \
            = (self._iterate_over_books(prompt))
        if read_book:
            if read_book['read']:
                print(f"The book {read_book['name'].title()} had already been "
                      f"marked as read before.")
            elif not read_book['read']:
                Book.mark_book_read(read_book['name'])
                print(f"The book {read_book['name'].title()} "
                      f"has been marked as read.")

    def prompt_delete_book(self):
        """
        Saves the prompt that is going to be passed to the _iterate method,
        call the _iterate by passing the prompt and saves the return in the
        book_to_delete variable. The return of iterate could be: 1. The book
        when the book is found or None if the book is not found or the list
        is empty. If a book is returned, the Book.delete_book is called,
        passing the name of the _iterate returned book as a parameter. Then,
        confirmation of the book deletion is given to the user.
        :return:
        """
        prompt = 'Write the name of the book you want to delete: -->  '
        book_to_delete: Union[dict[str, str | int], None] \
            = (self._iterate_over_books(prompt))
        if book_to_delete:
            Book.delete_book(book_to_delete['name'].lower())
            print(f"The book {book_to_delete['name'].title()} has been deleted")

    def _iterate_over_books(self, prompt: str) -> (
            Union)[dict[str, str | int], None]:
        """
        gets all the books from Book_get_all_books and saves them to books.
        If there is no vue returned by get_all_books, informs the user there
        are no books in the list yet and returns None so the method does not
        keep going. If _iterate does return something, then calls the
        self.list_books method to present the books to the user so they can
        see then and decide what to mark as read or delete. Then ask for the
        name of the target book and removes extra spaces and lowercase it.
        Iterates over books and finds a match for the prompt (name of the
        book) in the list of books. If found, returns the matched book,
        if not found, informs the user that the book is not in the list.
        :param prompt: Book to mark as read or to delete.
        :return: The book if found or None when not book found.
        """
        books = Book.get_all_books()
        if not books:
            print('There are no books yet in the list.')
            return None
        else:
            self.list_books()
            target_book = input(prompt).strip().lower()
            for book in books:
                if book['name'].lower() == target_book.lower():
                    return book
            print('The book your are searching for '
                  'does not match the books in your list.')

    def run_menu(self):
        """
        Runs a while buckle with the menu options, and it is ended once the
        user selects 'q'. When the user presses 'q', the quit_program method
        is called and closes the program using the sys module. For all other
        options in the menu, when the user selects an option, it first
        validates if that option is part of the self.menu_selection keys. If
        it is a variable called action is created and then the value of
        self.menu_selection[user_input] is saved there. So if the user
        selected 'a', the value hold by action is prompt_add_book (the value
        of the 'a' key in the self.menu_selection dict). Since the values of
        the self.menu_selection dict are the methods names, we add () to
        action to call the corresponding selected method.
        :return: None
        """
        while True:
            self.display_menu()
            user_input = input('Enter your choice: -->  ')
            if user_input in self.menu_selection:
                action = self.menu_selection[user_input]
                action()
            else:
                print(f"{user_input} is not a valid choice.")

    def quit_program(self):
        """
        Exists the program printing a message to the user and using the sys
        module with the sys.exit() method.
        :return:
        """
        print('The program has ended.')
        sys.exit()


if __name__ == '__main__':
    Menu().run_menu()  # The run_menu method in Menu class is run
    Book.create_book_table()  # A table is created to store book data.

