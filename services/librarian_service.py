from database import DatabaseManager


class LibrarianService:

    @staticmethod
    def add_new_book(isbn, title, author, subject, publication_date):
        db = DatabaseManager()

        book = db.fetch_query("SELECT * FROM books WHERE isbn = ?", (isbn,))
        if book:
            print(f"Error: Book with ISBN {isbn} already exists")
            db.close()
            return

        db.execute_query("INSERT INTO books (isbn, title, author, subject, publication_date) VALUES (?, ?, ?, ?, ?)",
                         (isbn, title, author, subject, publication_date)
                         )
        db.close()
        print(f"Success: Book '{title}' added to catalog.")
        return True

    @staticmethod
    def add_book_item(barcode, isbn, rack):
        db = DatabaseManager()
        item = db.fetch_query("SELECT * FROM book_items WHERE barcode = ?", (barcode,))
        if item:
            print(f"Error: Barcode {barcode} already exist")
            db.close()
            return

        book = db.fetch_query("SELECT * FROM books WHERE isbn = ?", (isbn,))
        if not book:
            print("Error: ISBN not in catalog.")
            db.close()
            return

        db.execute_query("INSERT INTO book_items (barcode, isbn, rack_number, status) VALUES (?, ?, ?, 'available')",
                         (barcode, isbn, rack))
        db.close()
        print(f"New book item {barcode} added to rack {rack}.")

    @staticmethod
    def edit_book(isbn, new_title=None, new_author=None, new_subject=None):
        db = DatabaseManager()

        book = db.fetch_query("SELECT * FROM books WHERE isbn = ?", (isbn,))
        if not book:
            print(f"Error: Book ISBN {isbn} not found.")
            db.close()
            return

        updates = []
        params = []

        if new_title:
            updates.append("title = ?")
            params.append(new_title)
        if new_author:
            updates.append("author = ?")
            params.append(new_author)
        if new_subject:
            updates.append("subject = ?")
            params.append(new_subject)

        if not updates:
            print("There is nothing to update")
            db.close()
            return

        params.append(isbn)
        query = f"UPDATE books SET {', '.join(updates)} WHERE isbn = ?"

        db.execute_query(query, tuple(params))
        db.close()
        print(f"Success: Book {isbn} details updated")

    @staticmethod
    def edit_book_item(barcode, new_rack=None, new_status=None):
        db = DatabaseManager()

        item = db.fetch_query("SELECT * FROM book_items WHERE barcode = ?", (barcode,))
        if not item:
            print(f"Error: Item {barcode} not found.")
            db.close()
            return

        updates = []
        params = []

        if new_rack:
            updates.append("rack_number = ?")
            params.append(new_rack)
        if new_status:
            updates.append("status = ?")
            params.append(new_status)

        if not updates:
            print("There is nothing to update")
            db.close()
            return

        params.append(barcode)
        query = f"UPDATE book_items SET {', '.join(updates)} WHERE barcode = ?"

        db.execute_query(query, tuple(params))
        db.close()
        print(f"Success: Item {barcode} updated")

    @staticmethod
    def remove_book(isbn):
        db = DatabaseManager()

        items = db.fetch_query("SELECT * FROM book_items WHERE isbn = ? AND status = 'loaned'", (isbn,))
        if items:
            print(f"Error: we can not remove this book as there are {len(items)} copies currently checked out")
            print("Please wait for all copies to be returned before removing this title")
            db.close()
            return

        db.execute_query("DELETE FROM book_items WHERE isbn = ?", (isbn,))
        db.execute_query("DELETE FROM books WHERE isbn = ?", (isbn,))
        db.close()

        print(f"Success: Book {isbn} and its items have been removed from the system")

    @staticmethod
    def remove_book_item(barcode):
        db = DatabaseManager()

        item = db.fetch_query("SELECT * FROM book_items WHERE barcode = ?", (barcode,))
        if not item:
            print(f"Error: Item {barcode} not found.")
            db.close()
            return

        if item[0][3] == 'loaned':
            print("Error: Cannot remove this book as it is currently checked out")
            db.close()
            return

        db.execute_query("DELETE FROM book_items WHERE barcode = ?", (barcode,))
        db.close()
        print(f"Success: Book item {barcode} removed.")

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

    @staticmethod
    def cancel_membership(member_id):
        db = DatabaseManager()

        member = db.fetch_query("SELECT checkout_count FROM members WHERE member_id = ?", (member_id,))
        if not member:
            print("Error: Member not found.")
            db.close()
            return

        if member[0][0] > 0:
            print("Error: We can not cancel this membership now as this member has books checked out currently")
            db.close()
            return

        db.execute_query("DELETE FROM members WHERE member_id = ?", (member_id,))
        db.close()
        print(f"Success: Membership cancelled for {member_id}.")


