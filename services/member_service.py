from datetime import datetime
from person import Member
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

        book_item = BookRepository.get_book_item(barcode)
        if not book_item or book_item[0][3] != 'available':
            print("ERROR: Book not available.")
            return False

        due_date = member.get_due_date()
        today = datetime.now().date()

        BookRepository.update_item_status(barcode, 'loaned')
        LoanRepository.create_loan(member.id, barcode, today, due_date)
        MemberRepository.update_checkout_count(member.id, increment=True)

        member.checkout_count += 1
        print(f"Success: book {barcode} checked out to {member.name} due to {due_date}")
        return True

    @staticmethod
    def return_book(member, barcode):
        loan = LoanRepository.get_active_loan_for_member(barcode, member.id)
        if not loan:
            print(f"ERROR: No active loan found for book {barcode}")
            return False

        loan_id = loan[0][0]
        due_date = datetime.strptime(loan[0][1], "%Y-%m-%d").date()
        today = datetime.now().date()
        fine = member.calculate_fine(today, due_date)

        LoanRepository.close_loan(loan_id, today, fine)
        BookRepository.update_item_status(barcode, 'available')
        MemberRepository.update_checkout_count(member.id, increment=False)
        member.checkout_count -= 1
        NotificationService.notify_reserved_members(barcode)
        print(f"Success: Book returned")
        return True

    @staticmethod
    def reserve_book(member, isbn):
        book = BookRepository.get_book_by_isbn(isbn)
        if not book:
            print(f"ERROR: book does not exist")
            return False

        today = datetime.now().date()
        MemberRepository.add_reservation(member.id, isbn, today)
        print(f"Success: Reserved '{book[0][0]}'.")
        return True

    @staticmethod
    def renew_book(member, barcode):
        loan = LoanRepository.get_active_loan_for_member(barcode, member.id)
        if not loan:
            print("No active loan found for this member.")
            return False

        loan_id = loan[0][0]

        info = BookRepository.get_book_item(barcode)
        if info:
            isbn = info[0][1]
            reservation = MemberRepository.get_waiting_reservation(isbn)
            if reservation:
                print(f"ERROR: This book {isbn} is reserved by another member.")
                return False

        new_due_date = member.get_due_date()
        LoanRepository.update_loan_due_date(loan_id, new_due_date)
        print(f"Success: Book renewed New due date: {new_due_date}")
        return True

    @staticmethod
    def cancel_reservation(member, isbn):
        reservation = MemberRepository.get_reservation(member.id, isbn)

        if not reservation:
            print("Error: There is no reservation found for this book")
            return False

        MemberRepository.cancel_reservation(member.id, isbn)

        notifier = EmailNotification()
        notifier.send(member, f"Your reservation for book (ISBN: {isbn}) has been successfully cancelled.")

        print(f"Success: Reservation for this book {isbn} is cancelled")
        return True

    @staticmethod
    def get_member_books(member_id):
        books = LoanRepository.get_borrowed_books_by_member(member_id)
        if not books:
            print(f"\nNo books currently checked out for member {member_id}")
            return False

        print(f"\nBooks Checked Out by {member_id}")
        for book in books:
            print(f"- Title: {book[0]} | Barcode: {book[1]} | Due: {book[2]}")

        return True
