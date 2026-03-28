from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository
from repositories.librarian_repository import LibrarianRepository


class LibrarianService:

    @staticmethod
    def add_new_book(isbn, title, author, subject, publication_date):
        book = BookRepository.get_book_by_isbn(isbn)
        if book:
            print(f"Error: Book with ISBN {isbn} already exists")
            return
        BookRepository.add_book(isbn, title, author, subject, publication_date)
        print(f"Success: Book '{title}' added to catalog.")

    @staticmethod
    def add_book_item(barcode, isbn, rack):
        item = BookRepository.get_book_item(barcode)
        if item:
            print(f"Error: Barcode {barcode} already exist")
            return
        book = BookRepository.get_book_by_isbn(isbn)
        if not book:
            print("Error: ISBN not in catalog.")
            return
        BookRepository.add_book_item(barcode, isbn, rack)
        print(f"New book item {barcode} added to rack {rack}.")

    @staticmethod
    def edit_book(isbn, new_title=None, new_author=None, new_subject=None):
        book = BookRepository.get_book_by_isbn(isbn)
        if not book:
            print(f"Error: Book ISBN {isbn} not found")
            return
        BookRepository.update_book(isbn, new_title, new_author, new_subject)
        print(f"Success: Book {isbn} details updated")

    @staticmethod
    def edit_book_item(barcode, new_rack=None, new_status=None):
        item = BookRepository.get_book_item(barcode)
        if not item:
            print(f"Error: Item {barcode} not found.")
            return
        BookRepository.update_book_item(barcode, new_rack, new_status)
        print(f"Success: Item {barcode} updated")

    @staticmethod
    def remove_book(isbn):
        items = BookRepository.get_items_by_isbn(isbn)
        loan = LoanRepository.get_active_loan_for_isbn(isbn)
        if loan:
            print(f"Error: we can not remove this book as there are {len(items)} copies currently checked out")
            print("Please wait for all copies to be returned before removing this title")
            return
        BookRepository.remove_items_by_isbn(isbn)
        BookRepository.remove_book(isbn)
        print(f"Success: Book {isbn} and its items have been removed from the system")

    @staticmethod
    def remove_book_item(barcode):
        item = BookRepository.get_book_item(barcode)
        if not item:
            print(f"Error: Item {barcode} not found.")
            return
        if item[0][3] == 'loaned':
            print("Error: Cannot remove this book as it is currently checked out")
            return
        BookRepository.remove_book_item(barcode)
        print(f"Success: Book item {barcode} removed.")

    @staticmethod
    def register_member(name, member_id, email, password="1234"):
        member = MemberRepository.get_member(member_id)
        if member:
            print(f"Error: Member {member_id} already exists")
            return False
        MemberRepository.add_member(name, member_id, email, password)
        print(f"Success: Member '{name}' registered with default password: {password}")
        return True

    @staticmethod
    def register_librarian(name, librarian_id, email, password):
        existing = LibrarianRepository.get_librarian(librarian_id)
        if existing:
            print(f"Error: Librarian {librarian_id} already exists")
            return
        LibrarianRepository.add_librarian(name, librarian_id, email, password)
        print(f"Success: Librarian '{name}' registered.")

    @staticmethod
    def get_book_borrower(barcode):
        member = LoanRepository.get_borrower_info(barcode)
        if member:
            print(f"Book {barcode} is currently borrowed by: {member[0][0]} (ID: {member[0][1]})")
            print(f"Email: {member[0][2]} | Due Date: {member[0][3]}")
        else:
            print(f"Book {barcode} is currently available (not checked out)")

    @staticmethod
    def get_borrowed_books(member_id):
        books = LoanRepository.get_borrowed_books_by_member(member_id)
        if not books:
            print(f"No books currently checked out for member {member_id}")
            return
        print(f"currently checked out books for member {member_id}")
        for book in books:
            print(f"Title: {book[0]} | Barcode: {book[1]} | Due: {book[2]}")

    @staticmethod
    def get_all_borrowed_books():
        books = LoanRepository.get_all_active_loans()
        if not books:
            print(f"No books currently checked out")
            return
        print(f"currently checked out books: {len(books)}")
        print(f"{'Member Name':<20} | {'Book Title':<25} | {'Barcode':<8} | {'Due Date'}")
        print("----------------------------------------------------------------------------")
        for book in books:
            print(f"{book[0][:18]:<20} | {book[2][:23]:<25} | {book[3]:<8} | {book[4]}")

    @staticmethod
    def cancel_membership(member_id):
        member = MemberRepository.get_member(member_id)
        if not member:
            print("Error: Member not found.")
            return
        if member[0][3] > 0:
            print("Error: We can not cancel this membership now as this member has books checked out currently")
            return
        MemberRepository.delete_member(member_id)
        print(f"Success: Membership cancelled for {member_id}")
