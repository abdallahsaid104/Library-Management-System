from database import DatabaseManager


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

    def __init__(self, name, person_id, email, checkout_count = 0):
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


class Librarian(Person):
    def __init__(self, name, employee_id, email):
        super().__init__(name, employee_id, email)

    @staticmethod
    def add_book_item(barcode, isbn, rack):
        db = DatabaseManager()
        query = "SELECT * FROM books WHERE isbn = ?"

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

