from datetime import datetime
from database import DatabaseManager
from services.notification_service import EmailNotification, NotificationService
from repositories.member_repository import MemberRepository
from repositories.book_repository import BookRepository
from repositories.loan_repository import LoanRepository


class MemberService:

    @staticmethod
    def checkout_book(member, barcode):
        if not member.can_checkout():
            print(f"ERROR: {member.name} has reached the maximum limit {member.MaxBooksLimit}")
            return False

        with DatabaseManager() as db:
            book_repo = BookRepository(db)
            loan_repo = LoanRepository(db)
            member_repo = MemberRepository(db)

            book_item = book_repo.get_book_item(barcode)
            item_status = book_item.status if book_item else None

            if not book_item or item_status != 'available':
                print("ERROR: Book not available.")
                return False

            due_date = member.get_due_date()
            today = datetime.now().date()

            book_repo.update_item_status(barcode, 'loaned')
            loan_repo.create_loan(member.id, barcode, today, due_date)
            member_repo.update_checkout_count(member.id, increment=True)

        member.checkout_count += 1
        print(f"Success: Book {barcode} checked out to {member.name} due to {due_date}")
        return True

    @staticmethod
    def return_book(member, barcode):
        with DatabaseManager() as db:
            loan_repo = LoanRepository(db)
            book_repo = BookRepository(db)
            member_repo = MemberRepository(db)

            loan = loan_repo.get_active_loan_for_member(barcode, member.id)
            if not loan:
                print(f"ERROR: No active loan found for book {barcode}")
                return False

            loan_id = loan[0][0]
            due_date_str = loan[0][1]
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

            today = datetime.now().date()
            fine = member.calculate_fine(today, due_date)

            loan_repo.close_loan(loan_id, today, fine)
            book_repo.update_item_status(barcode, 'available')
            member_repo.update_checkout_count(member.id, increment=False)

            NotificationService.notify_reserved_members(barcode)

        member.checkout_count -= 1
        print(f"Success: Book returned")
        return True

    @staticmethod
    def reserve_book(member, isbn):
        with DatabaseManager() as db:
            book_repo = BookRepository(db)
            member_repo = MemberRepository(db)

            book = book_repo.get_book_by_isbn(isbn)
            if not book:
                print("ERROR: Book does not exist")
                return False

            book_title = book.title
            today = datetime.now().date()
            member_repo.add_reservation(member.id, isbn, today)

        print(f"Success: Reserved '{book_title}'")
        return True

    @staticmethod
    def renew_book(member, barcode):
        with DatabaseManager() as db:
            loan_repo = LoanRepository(db)
            book_repo = BookRepository(db)
            member_repo = MemberRepository(db)

            loan = loan_repo.get_active_loan_for_member(barcode, member.id)
            if not loan:
                print("No active loan found for this member")
                return False

            loan_id = loan[0][0]

            info = book_repo.get_book_item(barcode)
            if info:
                isbn = info.isbn
                reservation = member_repo.get_waiting_reservation(isbn)
                if reservation:
                    print(f"ERROR: This book (ISBN: {isbn}) is reserved by another member")
                    return False

            new_due_date = member.get_due_date()
            loan_repo.update_loan_due_date(loan_id, new_due_date)

        print(f"Success: Book renewed ---> new due date: {new_due_date}")
        return True

    @staticmethod
    def cancel_reservation(member, isbn):
        with DatabaseManager() as db:
            member_repo = MemberRepository(db)

            reservation = member_repo.get_reservation(member.id, isbn)
            if not reservation:
                print("Error: There is no reservation found for this book")
                return False

            member_repo.cancel_reservation(member.id, isbn)

        notifier = EmailNotification()
        notifier.send(member, f"Your reservation for book (ISBN: {isbn}) has been successfully cancelled")

        print(f"Success: Reservation for book {isbn} is cancelled")
        return True

    @staticmethod
    def get_member_books(member_id):
        with DatabaseManager() as db:
            loan_repo = LoanRepository(db)
            books = loan_repo.get_borrowed_books_by_member(member_id)

        if not books:
            print(f"\nNo books currently checked out for member {member_id}")
            return False

        print(f"\nBooks Checked Out by {member_id}")
        for book in books:
            print(f"- Title: {book[0]} | Barcode: {book[1]} | Due: {book[2]}")

        return True

    @staticmethod
    def search_books(search_term, search_type):
        with DatabaseManager() as db:
            book_repo = BookRepository(db)
            return book_repo.search_books(search_term, search_type)

    @staticmethod
    def get_borrowed_books_list(member_id):
        with DatabaseManager() as db:
            loan_repo = LoanRepository(db)
            return loan_repo.get_borrowed_books_by_member(member_id)
