from datetime import datetime
from person import Member
from repositories.member_repository import MemberRepository
from repositories.book_repository import BookRepository
from repositories.loan_repository import LoanRepository


class Notification:
    def send(self, member, message):
        raise NotImplementedError("Subclass must implement this method")


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
        item = BookRepository.get_book_item(barcode)
        if not item:
            return

        isbn = item[0][1]
        reservation = MemberRepository.get_waiting_reservation(isbn)
        if reservation:
            member_id = reservation[0][0]
            member = Member.get_member(member_id)

            if member:
                notifier = EmailNotification()
                notifier.send(member, f"The book {isbn} you reserved is now available")
                MemberRepository.update_reservation_status(member.id, isbn, 'notified')

    @staticmethod
    def check_overdue():
        today = datetime.now().date()
        loans = LoanRepository.get_overdue_loans(today)

        if not loans:
            print("No overdue books found")
            return

        print(f"There is {len(loans)} overdue books")

        for loan in loans:
            member_id, barcode, due_date_str, title = loan
            member = Member.get_member(member_id)

            if member:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                notifier = EmailNotification()
                notifier.send(member, f"OVERDUE ALERT: '{title}' was due on {due_date}")
