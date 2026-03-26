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