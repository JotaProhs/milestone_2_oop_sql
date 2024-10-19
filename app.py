from utils.book import Book
import textwrap
import sys


class Menu:
    def __init__(self):
        self.menu_selection = {
            'a': self.prompt_add_book,
            'l': self.list_books,
            'r': self.prompt_read_book,
            'd': self.prompt_delete_book,
            'q': self.quit_program,
        }
        self.menu = textwrap.dedent("""
            - 'a' to add a new book.
            - 'l' to list all the books.
            - 'r' to mark a book as read.
            - 'd' to delete a book.
            - 'q' to quit
             """)
        self.chosen_option = None

    def display_menu(self):
        print(self.menu)

    def prompt_add_book(self):
        name = input('Write the name of the book: -->  ').strip()
        author = input('Write the name of the author: -->  ').strip()
        if not name or not author:
            print('Both, book name and author are required.')
        book = Book(name, author)
        book.create_book_table()
        if book.add_book():
            print(f"The book {name.title()} by {author.title()}"
                  f" has been added to your list.")
        else:
            print(f"The book {name.title()} by {author.title()}"
                  f" is already in the list. Duplicates not allowed.")
        return book

    def list_books(self):
        books = Book.get_all_books()
        if not books:
            print('There are no books in your list yet.')
        else:
            for i, book in enumerate(books, start=1):
                read = ('Already read.' if book['read'] else 'Not read yet.')
                print(f"{i}. {book['name'].title()} by "
                      f"{book['author'].title()} - {read}")

    def prompt_read_book(self):
        prompt = 'Write the name of the book you want to mark as read: -->  '
        read_book = self._iterate_over_books(prompt)
        if read_book:
            if read_book['read']:
                print(f"The book {read_book['name'].title()} had already been "
                      f"marked as read before.")
            else:
                Book.mark_book_read(read_book['name'])
                print(f"The book {read_book['name'].title()} "
                      f"has been marked as read.")
        else:
            print('The name of the book provided does not mats any of the books')

    def prompt_delete_book(self):
        prompt = 'Write the name of the book you want to delete: -->  '
        book_to_delete = self._iterate_over_books(prompt)
        if book_to_delete:
            Book.delete_book(book_to_delete['name'].lower())
            print(f"The book {book_to_delete['name'].title()} has been deleted")
        else:
            print('The name of the book provided does not '
                  'match any of the books in your list.')

    def _iterate_over_books(self, prompt):
        books = Book.get_all_books()
        if not books:
            print('There are no books in your list yet.')
            return None
        else:
            self.list_books()
            target_book = input(prompt).strip().lower()
            for book in books:
                if book['name'].lower() == target_book.lower():
                    return book
            return None

    def run_menu(self):
        while True:
            self.display_menu()
            user_input = input('Enter your choice: -->  ')
            if user_input in self.menu_selection:
                action = self.menu_selection[user_input]
                action()
            else:
                print(f"{user_input} is not a valid choice.")

    def quit_program(self):
        print('The program has ended.')
        sys.exit()


if __name__ == '__main__':
    Menu().run_menu()

