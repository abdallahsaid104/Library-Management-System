from database import DatabaseManager
from services.notification_service import NotificationService
from person import Member
from datetime import datetime


class MemberService:

    @staticmethod
    def checkout_book(member, barcode):
        if not member.can_checkout():
            print(f"ERROR: {member.name} has reached the maximum limit {member.MaxBooksLimit}")
            return

        db = DatabaseManager()
        item = db.fetch_query("SELECT * FROM book_items WHERE barcode = ? AND status = 'available'", (barcode,))
        if not item:
            print(f"ERROR: Book item {barcode} is not available.")
            db.close()
            return

        due_date = member.get_due_date()
        today = datetime.now().date()

        db.execute_query("UPDATE book_items SET status = 'loaned' WHERE barcode = ?", (barcode,))

        db.execute_query("INSERT INTO loans (member_id, book_barcode, issue_date, due_date) VALUES (?, ?, ?, ?)",
                         (member.id, barcode, str(today), str(due_date)))

        db.execute_query("UPDATE members SET checkout_count = checkout_count + 1 WHERE member_id = ?", (member.id,))
        db.close()

        member.checkout_count += 1
        print(f"Success: book {barcode} checked out to {member.name} due to {due_date}")

    @staticmethod
    def return_book(member, barcode):
        db = DatabaseManager()
        loan = db.fetch_query(
            "SELECT loan_id, due_date FROM loans WHERE book_barcode = ? AND member_id = ? AND return_date IS NULL",
            (barcode, member.id)
        )
        if not loan:
            print(f"ERROR: No active loan found for book {barcode}")
            db.close()
            return

        loan_id = loan[0][0]
        due_date = datetime.strptime(loan[0][1], "%Y-%m-%d").date()
        today = datetime.now().date()
        fine = member.calculate_fine(today, due_date)

        db.execute_query("UPDATE loans SET return_date = ?, fine_amount = ? WHERE loan_id = ?",
                         (str(today), fine, loan_id))
        db.execute_query("UPDATE book_items SET status = 'available' WHERE barcode = ?", (barcode,))
        db.execute_query("UPDATE members SET checkout_count = checkout_count - 1 WHERE member_id = ?", (member.id,))

        NotificationService.notify_reserved_members(db, barcode)

        db.close()
        member.checkout_count -= 1
        print(f"Success: Book returned.")

    @staticmethod
    def reserve_book(member, isbn):
        db = DatabaseManager()
        book = db.fetch_query("SELECT title FROM books WHERE isbn = ?", (isbn,))
        if not book:
            print(f"ERROR: book does not exist")
            db.close()
            return

        today = datetime.now().date()
        db.execute_query("INSERT INTO reservations (member_id, isbn, reservation_date) VALUES (?, ?, ?)",
                         (member.id, isbn, str(today)))
        print(f"Success: Reserved '{book[0][0]}'.")
        db.close()

    @staticmethod
    def renew_book(member, barcode):
        db = DatabaseManager()

        loan = db.fetch_query(
            "SELECT loan_id, due_date FROM loans WHERE book_barcode = ? AND member_id = ? AND return_date IS NULL",
            (barcode, member.id)
        )

        if not loan:
            print("No active loan found for this member.")
            db.close()
            return

        loan_id = loan[0][0]

        # Check if someone reserved it (No allow if it reserved)
        info = db.fetch_query("SELECT isbn FROM book_items WHERE barcode = ?", (barcode,))
        if info:
            isbn = info[0][0]
            reservation = db.fetch_query("SELECT * FROM reservations WHERE isbn = ? AND status = 'waiting' LIMIT 1",
                                         (isbn,))
            if reservation:
                print(f"ERROR: This book {isbn} is reserved by another member.")
                db.close()
                return

        new_due_date = member.get_due_date()

        db.execute_query("UPDATE loans SET due_date = ? WHERE loan_id = ?", (str(new_due_date), loan_id))
        db.close()

        print(f"Success: Book renewed New due date: {new_due_date}")

    @staticmethod
    def cancel_reservation(member, isbn):
        db = DatabaseManager()

        reservation = db.fetch_query(
            "SELECT * FROM reservations WHERE member_id = ? AND isbn = ? AND status = 'waiting'",
            (member.id, isbn)
            )

        if not reservation:
            print("Error: There is no reservation found for this book")
            db.close()
            return

        db.execute_query(
            "DELETE FROM reservations WHERE member_id = ? AND isbn = ? AND status = 'waiting'",
            (member.id, isbn)
        )
        db.close()
        print(f"Success: Reservation for this book {isbn} is cancelled")
