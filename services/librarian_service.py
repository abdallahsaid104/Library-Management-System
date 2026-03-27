from database import DatabaseManager


class LibrarianService:
    @staticmethod
    def add_book_item(barcode, isbn, rack):
        db = DatabaseManager()

        if db.fetch_query("SELECT * FROM book_items WHERE barcode = ?", (barcode,)):
            print(f"Error: Barcode {barcode} already exist")
            db.close()
            return

        if not db.fetch_query("SELECT * FROM books WHERE isbn = ?", (isbn,)):
            print("Error: ISBN not in catalog.")
            db.close()
            return

        db.execute_query("INSERT INTO book_items (barcode, isbn, rack_number, status) VALUES (?, ?, ?, 'available')",
                         (barcode, isbn, rack))
        db.close()
        print(f"New book item {barcode} added to rack {rack}.")

    @staticmethod
    def register_member(name, member_id, email):
        db = DatabaseManager()

        if db.fetch_query("SELECT * FROM members WHERE member_id = ?", (member_id,)):
            print(f"Error: Member {member_id} already exists")
            db.close()
            return

        db.execute_query("INSERT INTO members (name, member_id, email, checkout_count) VALUES (?, ?, ?, 0)",
                         (name, member_id, email)
                         )
        db.close()
        print(f"Success: Member '{name}' registered.")

    @staticmethod
    def get_book_borrower(barcode):
        db = DatabaseManager()

        query = """SELECT m.name, m.member_id, m.email, l.due_date FROM loans l
                JOIN members m ON l.member_id = m.member_id WHERE l.book_barcode = ? AND l.return_date IS NULL"""
        books = db.fetch_query(query, (barcode,))
        db.close()

        if books:
            book = books[0]
            print(f"Book {barcode} is currently borrowed by: {book[0]} (ID: {book[1]})")
            print(f"Email: {book[2]} | Due Date: {book[3]}")
        else:
            print(f"Book {barcode} is currently available (not checked out).")

    @staticmethod
    def get_borrowed_books(member_id):
        db = DatabaseManager()

        query = """SELECT b.title, l.book_barcode, l.due_date FROM loans l JOIN book_items bi ON l.book_barcode = bi.barcode
                    JOIN books b ON bi.isbn = b.isbn WHERE l.member_id = ? AND l.return_date IS NULL"""
        books = db.fetch_query(query, (member_id,))
        db.close()

        if not books:
            print(f"No books currently checked out for member {member_id}")
            return

        print(f"currently checked out books for member {member_id}")
        for book in books:
            print(f"Title: {book[0]} | Barcode: {book[1]} | Due: {book[2]}")

    @staticmethod
    def get_all_borrowed_books():
        db = DatabaseManager()

        query = """SELECT m.name, m.member_id, b.title, l.book_barcode, l.due_date FROM loans l
                    JOIN members m ON l.member_id = m.member_id 
                    JOIN book_items bi ON l.book_barcode = bi.barcode
                    JOIN books b ON bi.isbn = b.isbn WHERE l.return_date IS NULL ORDER BY l.due_date ASC"""

        books = db.fetch_query(query)
        db.close()

        if not books:
            print(f"No books currently checked out")
            return

        print(f"currently checked out books: {len(books)}")
        print(f"{'Member Name':<20} | {'Book Title':<25} | {'Barcode':<8} | {'Due Date'}")
        print("----------------------------------------------------------------------------")
        for book in books:
            print(f"{book[0][:18]:<20} | {book[2][:23]:<25} | {book[3]:<8} | {book[4]}")
