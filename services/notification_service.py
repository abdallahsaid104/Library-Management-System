from person import Member
from database import DatabaseManager
from datetime import datetime


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
    def notify_reserved_members(db, barcode):
        item = db.fetch_query("SELECT isbn FROM book_items WHERE barcode = ?", (barcode,))
        if not item:
            return

        isbn = item[0][0]
        reservation = db.fetch_query("SELECT member_id FROM reservations WHERE isbn = ? AND status = 'waiting' LIMIT 1",
                                     (isbn,))
        if reservation:
            member_id = reservation[0][0]
            member = Member.get_member(member_id)
            if member:
                notifier = EmailNotification()
                notifier.send(member, f"The book {isbn} you reserved is now available")

                db.execute_query("UPDATE reservations SET status = 'notified' WHERE member_id = ? AND isbn = ?",
                                 (member.id, isbn))

    @staticmethod
    def check_overdue():
        db = DatabaseManager()
        today = datetime.now().date()

        query = """ SELECT l.member_id, l.book_barcode, l.due_date, b.title FROM loans l
                    JOIN book_items bi ON l.book_barcode = bi.barcode
                    JOIN books b ON bi.isbn = b.isbn WHERE l.return_date IS NULL AND l.due_date < ?
                """
        loans = db.fetch_query(query, (str(today),))
        db.close()

        if not loans:
            print("No overdue books found")
            return

        print(f"There is {le(loans)} overdue books")

        for loan in loans:
            member_id, barcode, due_date, title = loan
            member = Member.get_member(member_id)

            if member:
                due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

                notifier = EmailNotification()
                notifier.send(member, f"OVERDUE ALERT: '{title}' was due on {due_date}")

