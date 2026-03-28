from database import DatabaseManager
from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository
from repositories.librarian_repository import LibrarianRepository


class LibrarianService:

    @staticmethod
    def add_new_book(isbn, title, author, subject, publication_date):
        with DatabaseManager() as db:
            repo = BookRepository(db)

            if repo.get_book_by_isbn(isbn):
                print(f"Error: Book with ISBN {isbn} already exists")
                return False

            repo.add_book(isbn, title, author, subject, publication_date)
            print(f"Success: Book '{title}' added to catalog.")
        return True

    @staticmethod
    def add_book_item(barcode, isbn, rack):
        with DatabaseManager() as db:
            repo = BookRepository(db)
            if repo.get_book_item(barcode):
                print(f"Error: Barcode {barcode} already exists")
                return False

            if not repo.get_book_by_isbn(isbn):
                print("Error: ISBN not in catalog")
                return False

            repo.add_book_item(barcode, isbn, rack)
            print(f"New book item {barcode} added to rack {rack}.")
        return True

    @staticmethod
    def edit_book(isbn, new_title=None, new_author=None, new_subject=None):
        with DatabaseManager() as db:
            repo = BookRepository(db)

            if not repo.get_book_by_isbn(isbn):
                print(f"Error: Book ISBN {isbn} not found")
                return False

            repo.update_book(isbn, new_title, new_author, new_subject)
            print(f"Success: Book {isbn} details updated")
        return True

    @staticmethod
    def edit_book_item(barcode, new_rack=None, new_status=None):
        with DatabaseManager() as db:
            repo = BookRepository(db)

            if not repo.get_book_item(barcode):
                print(f"Error: Item {barcode} not found.")
                return False

            repo.update_book_item(barcode, new_rack, new_status)
            print(f"Success: Item {barcode} updated")
        return True

    @staticmethod
    def remove_book(isbn):
        with DatabaseManager() as db:
            book_repo = BookRepository(db)
            loan_repo = LoanRepository(db)

            active_loans = loan_repo.get_active_loan_for_isbn(isbn)
            if active_loans:
                print(f"Error: Cannot remove this book as there are {len(active_loans)} copies currently checked out.")
                print("Please wait for all copies to be returned before removing this title.")
                return False

            book_repo.remove_items_by_isbn(isbn)
            book_repo.remove_book(isbn)
            print(f"Success: Book {isbn} and its items have been removed from the system")
        return True

    @staticmethod
    def remove_book_item(barcode):
        with DatabaseManager() as db:
            repo = BookRepository(db)
            item = repo.get_book_item(barcode)
            if not item:
                print(f"Error: Item {barcode} not found.")
                return False

            if item[0][3] == 'loaned':
                print("Error: Cannot remove this book as it is currently checked out")
                return False
            repo.remove_book_item(barcode)
            print(f"Success: Book item {barcode} removed")
        return True

    @staticmethod
    def register_member(name, member_id, email, password="1234"):
        with DatabaseManager() as db:
            repo = MemberRepository(db)
            if repo.get_member(member_id):
                print(f"Error: Member {member_id} already exists")
                return False
            repo.add_member(name, member_id, email, password)
            print(f"Success: Member '{name}' registered with default password: {password}")
        return True

    @staticmethod
    def register_librarian(name, librarian_id, email, password):
        with DatabaseManager() as db:
            repo = LibrarianRepository(db)

            existing = repo.get_librarian(librarian_id)
            if existing:
                print(f"Error: Librarian {librarian_id} already exists")
                return False

            repo.add_librarian(name, librarian_id, email, password)
            print(f"Success: Librarian '{name}' registered.")
        return True

    @staticmethod
    def get_book_borrower(barcode):
        with DatabaseManager() as db:
            repo = LoanRepository(db)
            member = repo.get_borrower_info(barcode)
            if not member:
                print(f"Book {barcode} is currently available (not checked out)")
                return False

            print(f"Book {barcode} is currently borrowed by: {member[0][0]} (ID: {member[0][1]})")
            print(f"Email: {member[0][2]} | Due Date: {member[0][3]}")
        return True

    @staticmethod
    def get_borrowed_books(member_id):
        with DatabaseManager() as db:
            repo = LoanRepository(db)
            books = repo.get_borrowed_books_by_member(member_id)
            if not books:
                print(f"No books currently checked out for member {member_id}")
                return False
            print(f"Currently checked out books for member {member_id}")
            for book in books:
                print(f"Title: {book[0]} | Barcode: {book[1]} | Due: {book[2]}")
        return True

    @staticmethod
    def get_all_borrowed_books():
        with DatabaseManager() as db:
            repo = LoanRepository(db)
            books = repo.get_all_active_loans()
            if not books:
                print("No books currently checked out")
                return False
            print(f"currently checked out books: {len(books)}")
            print(f"{'Member Name':<20} | {'Book Title':<25} | {'Barcode':<8} | {'Due Date'}")
            print("----------------------------------------------------------------------------")
            for book in books:
                print(f"{book[0][:18]:<20} | {book[2][:23]:<25} | {book[3]:<8} | {book[4]}")
        return True

    @staticmethod
    def cancel_membership(member_id):
        with DatabaseManager() as db:
            repo = MemberRepository(db)
            member = repo.get_member(member_id)
            if not member:
                print("Error: Member not found")
                return False
            checkout_count = member[0][3]
            if checkout_count > 0:
                print("Error: We can not cancel this membership now as this member has books checked out currently")
                return False
            repo.delete_member(member_id)
            print(f"Success: Membership cancelled for {member_id}")
        return True
