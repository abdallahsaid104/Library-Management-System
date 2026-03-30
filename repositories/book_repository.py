from models.book import Book, BookItem


class BookRepository:

    def __init__(self, db):
        self.db = db

    def search_books(self, search_term, search_type):
        allowed_types = {"title", "author", "subject", "publication_date"}
        if search_type not in allowed_types:
            raise ValueError(f"Invalid search type: {search_type}")

        books = self.db.fetch_query(f"SELECT * FROM books WHERE {search_type} LIKE ?", (f"%{search_term}%",))
        return [Book.from_db_row(book) for book in books] if books else None

    def get_book_item(self, barcode):
        item = self.db.fetch_query("SELECT * FROM book_items WHERE barcode = ?", (barcode,))
        return BookItem.from_db_row(item[0]) if item else None

    def update_item_status(self, barcode, status):
        self.db.execute_query("UPDATE book_items SET status = ? WHERE barcode = ?", (status, barcode))

    def get_book_by_isbn(self, isbn):
        book = self.db.fetch_query("SELECT * FROM books WHERE isbn = ?", (isbn,))
        return Book.from_db_row(book[0]) if book else None

    def get_items_by_isbn(self, isbn):
        items = self.db.fetch_query("SELECT * FROM book_items WHERE isbn = ?", (isbn,))
        return [BookItem.from_db_row(item) for item in items] if items else None

    def add_book(self, isbn, title, author, subject, pub_date):
        self.db.execute_query("INSERT INTO books VALUES (?, ?, ?, ?, ?)", (isbn, title, author, subject, pub_date))

    def update_book(self, isbn, title=None, author=None, subject=None):
        updates = []
        params = []
        fields_to_update = {
            "title": title,
            "author": author,
            "subject": subject
        }
        for field_type, value in fields_to_update.items():
            if value is not None:
                updates.append(f"{field_type} = ?")
                params.append(value)

        if not updates:
            raise ValueError("No fields provided to update")

        params.append(isbn)
        self.db.execute_query(f"UPDATE books SET {', '.join(updates)} WHERE isbn = ?", tuple(params))

    def remove_book(self, isbn):
        self.db.execute_query("DELETE FROM books WHERE isbn = ?", (isbn,))

    def add_book_item(self, barcode, isbn, rack):
        self.db.execute_query(
            "INSERT INTO book_items (barcode, isbn, rack_number, status) VALUES (?, ?, ?, 'available')",
            (barcode, isbn, rack)
        )

    def remove_book_item(self, barcode):
        self.db.execute_query("DELETE FROM book_items WHERE barcode = ?", (barcode,))

    def remove_items_by_isbn(self, isbn):
        self.db.execute_query("DELETE FROM book_items WHERE isbn = ?", (isbn,))

    def update_book_item(self, barcode, rack=None, status=None):
        updates = []
        params = []
        fields_to_update = {
            "rack": rack,
            "status": status
        }

        for field_type, value in fields_to_update.items():
            if value is not None:
                updates.append(f"{field_type} = ?")
                params.append(value)

        if not updates:
            raise ValueError("No fields provided to update")

        params.append(barcode)
        self.db.execute_query(f"UPDATE book_items SET {', '.join(updates)} WHERE barcode = ?", tuple(params))
