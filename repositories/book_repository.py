from database import DatabaseManager


class BookRepository:

    @staticmethod
    def search_books(search_term, search_type):
        db = DatabaseManager()
        query = f"SELECT * FROM books WHERE {search_type} LIKE ?"
        param = f"%{search_term}%"
        books = db.fetch_query(query, (param,))
        db.close()
        return books

    @staticmethod
    def get_book_item(barcode):
        db = DatabaseManager()
        item = db.fetch_query("SELECT * FROM book_items WHERE barcode = ?", (barcode,))
        db.close()
        return item

    @staticmethod
    def update_item_status(barcode, status):
        db = DatabaseManager()
        db.execute_query("UPDATE book_items SET status = ? WHERE barcode = ?", (status, barcode))
        db.close()

    @staticmethod
    def get_book_by_isbn(isbn):
        db = DatabaseManager()
        result = db.fetch_query("SELECT * FROM books WHERE isbn = ?", (isbn,))
        db.close()
        return result

    @staticmethod
    def add_book(isbn, title, author, subject, pub_date):
        db = DatabaseManager()
        db.execute_query(
            "INSERT INTO books VALUES (?, ?, ?, ?, ?)",
            (isbn, title, author, subject, pub_date)
        )
        db.close()

    @staticmethod
    def update_book(isbn, title=None, author=None, subject=None):
        db = DatabaseManager()
        updates = []
        params = []
        if title:
            updates.append("title = ?")
            params.append(title)
        if author:
            updates.append("author = ?")
            params.append(author)
        if subject:
            updates.append("subject = ?")
            params.append(subject)

        if updates:
            query = f"UPDATE books SET {', '.join(updates)} WHERE isbn = ?"
            params.append(isbn)
            db.execute_query(query, tuple(params))
        db.close()

    @staticmethod
    def remove_book(isbn):
        db = DatabaseManager()
        db.execute_query("DELETE FROM books WHERE isbn = ?", (isbn,))
        db.close()

    @staticmethod
    def add_book_item(barcode, isbn, rack):
        db = DatabaseManager()
        db.execute_query(
            "INSERT INTO book_items (barcode, isbn, rack_number, status) VALUES (?, ?, ?, 'available')",
            (barcode, isbn, rack)
        )
        db.close()

    @staticmethod
    def remove_book_item(barcode):
        db = DatabaseManager()
        db.execute_query("DELETE FROM book_items WHERE barcode = ?", (barcode,))
        db.close()

    @staticmethod
    def remove_items_by_isbn(isbn):
        db = DatabaseManager()
        db.execute_query("DELETE FROM book_items WHERE isbn = ?", (isbn,))
        db.close()

    @staticmethod
    def update_book_item(barcode, rack=None, status=None):
        db = DatabaseManager()
        updates = []
        params = []
        if rack:
            updates.append("rack_number = ?")
            params.append(rack)
        if status:
            updates.append("status = ?")
            params.append(status)

        if updates:
            query = f"UPDATE book_items SET {', '.join(updates)} WHERE barcode = ?"
            params.append(barcode)
            db.execute_query(query, tuple(params))
        db.close()
