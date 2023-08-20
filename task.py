from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, isbn, total_copies):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = total_copies


class Patron:
    def __init__(self, name, patron_id):
        self.name = name
        self.patron_id = patron_id
        self.borrowed_books = []


class Library:
    def __init__(self):
        self.books = []
        self.patrons = []

    def add_book(self, book):
        self.books.append(book)

    def add_patron(self, patron):
        self.patrons.append(patron)

    def borrow_book(self, patron, book):
        if book.available_copies > 0:
            book.available_copies -= 1
            patron.borrowed_books.append(book)
            print(f"{patron.name} has borrowed '{book.title}' by {book.author}.")
            return True
        else:
            print(f"Sorry, '{book.title}' is not available for borrowing.")
            return False

    def return_book(self, patron, book):
        if book in patron.borrowed_books:
            patron.borrowed_books.remove(book)
            book.available_copies += 1
            print(f"{patron.name} has returned '{book.title}' by {book.author}.")
            return True
        else:
            print(f"{patron.name} cannot return '{book.title}' as they didn't borrow it.")
            return False

    def display_books(self):
        print("Available Books:")
        for book in self.books:
            print(f"{book.title} by {book.author} - ISBN: {book.isbn} - Available Copies: {book.available_copies}")

    def display_patrons(self):
        print("Patrons:")
        for patron in self.patrons:
            print(f"{patron.name} (ID: {patron.patron_id})")

    def calculate_fine(self, patron):
        total_fine = 0
        current_date = datetime.now()

        for borrowed_book in patron.borrowed_books:
            due_date = current_date + timedelta(days=7)  # Due date is 1 weeks from now
            if current_date > due_date:
                days_overdue = (current_date - due_date).days
                fine = days_overdue * 3  # $3 per day overdue
                total_fine += fine
                print(f"{patron.name} has an overdue book '{borrowed_book.title}' with a fine of ${fine}.")

        if total_fine == 0:
            print(f"{patron.name} has no overdue books.")


class Catalog:
    def __init__(self, library):
        self.library = library

    def display_all_books(self):
        self.library.display_books()

    def display_all_patrons(self):
        self.library.display_patrons()


class Administrator:
    def __init__(self, library):
        self.library = library

    def add_book(self, title, author, isbn, total_copies):
        book = Book(title, author, isbn, total_copies)
        self.library.add_book(book)

    def remove_book(self, title):
        book_to_remove = None
        for book in self.library.books:
            if book.title == title:
                book_to_remove = book
                break
        if book_to_remove:
            self.library.books.remove(book_to_remove)
            print(f"'{book_to_remove.title}' by {book_to_remove.author} has been removed from the library.")
        else:
            print(f"Sorry, '{title}' is not found in the library.")

    def add_patron(self, name, patron_id):
        patron = Patron(name, patron_id)
        self.library.add_patron(patron)

    def remove_patron(self, patron_id):
        patron_to_remove = None
        for patron in self.library.patrons:
            if patron.patron_id == patron_id:
                patron_to_remove = patron
                break
        if patron_to_remove:
            self.library.patrons.remove(patron_to_remove)
            print(
                f"{patron_to_remove.name} (ID: {patron_to_remove.patron_id}) has been removed from the patron records.")
        else:
            print(f"Sorry, patron with ID {patron_id} is not found in the patron records.")


# Example usage
library = Library()
administrator = Administrator(library)
catalog = Catalog(library)

administrator.add_book("Confess", "Collen Hoover", "978-0743273565", 3)
administrator.add_book("ABC", "Maaz", "978-0061120084", 2)

administrator.add_patron("Aliza", 1)
administrator.add_patron("Minahil", 2)

catalog.display_all_books()
catalog.display_all_patrons()

library.borrow_book(library.patrons[0], library.books[0])
library.borrow_book(library.patrons[1], library.books[0])
library.return_book(library.patrons[0], library.books[0])
library.borrow_book(library.patrons[1], library.books[0])

catalog.display_all_books()
catalog.display_all_patrons()

library.calculate_fine(library.patrons[0])
library.calculate_fine(library.patrons[1])

administrator.remove_book("Confess")
administrator.remove_patron(2)

catalog.display_all_books()
catalog.display_all_patrons()

