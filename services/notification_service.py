from abc import ABC, abstractmethod
from datetime import datetime
from person import Member
from repositories.member_repository import MemberRepository
from repositories.book_repository import BookRepository
from repositories.loan_repository import LoanRepository
from database import DatabaseManager


class Notification(ABC):
    @abstractmethod
    def send(self, member, message):
        pass


class EmailNotification(Notification):
    def send(self, member, message):
        print(f"\n[EMAIL SENDING] To: {member.email}")
        print(f"  Subject: Library Notification")
        print(f"  Body: {message}")
        print("[EMAIL SENT SUCCESSFULLY]")


class SMSNotification(Notification):
    def send(self, member, message):
        print(f"\n[SMS SENDING] To: {member.id} ({member.name})")
        print(f"  Msg: {message}")
        print("[SMS SENT SUCCESSFULLY]")


class NotificationService:

    @staticmethod
    def notify_reserved_members(barcode):
        with DatabaseManager() as db:
            book_repo = BookRepository(db)
            member_repo = MemberRepository(db)

            item = book_repo.get_book_item(barcode)
            if not item:
                return

            isbn = item[0][1]
            reservation = member_repo.get_waiting_reservation(isbn)

            if reservation:
                member_id = reservation[0][0]
                member_data = member_repo.get_member(member_id)
                if member_data:
                    member = Member(*member_data[0])
                    notifier = EmailNotification()
                    notifier.send(member, f"The book {isbn} you reserved is now available")
                    member_repo.update_reservation_status(member.id, isbn, 'notified')

    @staticmethod
    def check_overdue():
        with DatabaseManager() as db:
            loan_repo = LoanRepository(db)
            member_repo = MemberRepository(db)

            today = datetime.now().date()
            loans = loan_repo.get_overdue_loans(today)

            if not loans:
                print("No overdue books found")
                return False

            print(f"There is {len(loans)} overdue books")
            for loan in loans:
                member_id, barcode, due_date_str, title = loan
                member_data = member_repo.get_member(member_id)
                if member_data:
                    member = Member(member_data[0][0], member_data[0][1], member_data[0][2], member_data[0][3],
                                    member_data[0][4])
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    notifier = EmailNotification()
                    notifier.send(member, f"OVERDUE ALERT: '{title}' was due on {due_date}")
        return True
