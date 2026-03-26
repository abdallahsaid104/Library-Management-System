from database import DatabaseManager
from datetime import datetime, timedelta


class Person:
    def __init__(self, name, person_id, email):
        self.name = name
        self.id = person_id
        self.email = email

    def __str__(self):
        info = f"""
Name: {self.name}
ID:   {self.id}
Email:{self.email}"""
        return info


class Member(Person):
    MaxBooksLimit = 5
    MaxDaysLimit = 10
    FinePerDay = 5

    def __init__(self, name, person_id, email, checkout_count=0):
        super().__init__(name, person_id, email)
        self.checkout_count = checkout_count

    def can_checkout(self):
        return self.checkout_count < self.MaxBooksLimit

    @staticmethod
    def get_member(member_id):
        db = DatabaseManager()
        query = "SELECT * FROM members WHERE member_id = ?"
        member = db.fetch_query(query, (member_id,))
        db.close()
        if member:
            return Member(member[0][0], member[0][1], member[0][2], member[0][3])
        return None

    def checkout_book(self, barcode):
        if not self.can_checkout():
            print(f"ERROR: {self.name} has reached the maximum number of books({self.MaxBooksLimit} books)")
            return False

        db = DatabaseManager()
        query = "SELECT * FROM book_items WHERE barcode = ? AND status = 'available'"
        item = db.fetch_query(query, (barcode,))

        if not item:
            print(f"ERROR: book item {barcode} is not available")
            db.close()
            return False

        query = "UPDATE book_items SET status = 'loaned' WHERE barcode = ?"
        db.execute_query(query, (barcode,))

        today = datetime.now().date()
        due_date = today + timedelta(days=self.MaxDaysLimit)

        query = "INSERT INTO loans (member_id, book_barcode, issue_date, due_date) VALUES (? , ?, ?, ?)"
        db.execute_query(query, (self.id, barcode, str(today), str(due_date)))

        query = "UPDATE members SET checkout_count = checkout_count + 1 WHERE member_id = ?"
        db.execute_query(query, (self.id,))
        self.checkout_count += 1

        db.close()
        print(f"Success: book {barcode} checked out to {self.name} due to {due_date}")

        return True

    def return_book(self, barcode):
        db = DatabaseManager()

        query = "SELECT loan_id, due_date FROM loans WHERE book_barcode = ? AND return_date IS NULL"
        loan = db.fetch_query(query, (barcode,))

        if not loan:
            print(f"ERROR: No active loan found for book {barcode}")
            db.close()
            return False

        loan_id = loan[0][0]
        due_date = datetime.strptime(loan[0][1], "%Y-%m-%d").date()
        today = datetime.now().date()
        fine = self.calculate_fine(today, due_date)
        self.update_db_on_return(db, barcode, loan_id, today, fine)

        return True

    def update_db_on_return(self, db: DatabaseManager, barcode, loan_id, today, fine):
        query = "UPDATE loans SET return_date = ?, fine_amount = ? WHERE loan_id = ?"
        db.execute_query(query, (str(today), fine, loan_id))

        query = "UPDATE book_items SET status = 'available' WHERE barcode = ?"
        db.execute_query(query, (barcode,))

        query = "UPDATE members SET checkout_count = checkout_count - 1 WHERE member_id = ?"
        db.execute_query(query, (self.id,))
        self.checkout_count -= 1

        db.close()
        print(f"Success: Book {barcode} returned.")

    def calculate_fine(self, today, due_date):
        fine = 0
        if today > due_date:
            days_late = (today-due_date).days
            fine = days_late * self.FinePerDay
            print(f"Book is {days_late} days late : Fine ----> {fine} Egyptian bound")
        else:
            print(f"Book is returned on time, No Fine")

        return fine

    @staticmethod
    def get_borrowed_books(member_id):
        db = DatabaseManager()
        query = """
            SELECT b.title, l.book_barcode, l.due_date FROM loans l
            JOIN book_items bi ON l.book_barcode = bi.barcode 
            JOIN books b ON bi.isbn = b.isbn WHERE l.member_id = ? AND l.return_date IS NULL
        """
        borrowed_books = db.fetch_query(query, (member_id,))
        db.close()
        return borrowed_books


class Librarian(Person):
    def __init__(self, name, employee_id, email):
        super().__init__(name, employee_id, email)

    @staticmethod
    def add_book_item(barcode, isbn, rack):
        db = DatabaseManager()
        query = "SELECT * FROM book_items WHERE barcode = ?"

        if db.fetch_query(query, (barcode,)):
            print(f"Error: Barcode {barcode} already exist")
            db.close()
            return

        if not db.fetch_query(query, (isbn,)):
            print("Error: Book ISBN does not exist in catalog")
            db.close()
            return

        query = "INSERT INTO book_items (barcode, isbn, rack_number, status) VALUES (?, ?, ?, 'available')"
        db.execute_query(query, (barcode, isbn, rack))
        db.close()
        print(f"New book item {barcode} added to rack {rack}.")


