from database import DatabaseManager
from person import Librarian


class LibrarianRepository:

    def __init__(self, db):
        self.db = db

    def get_librarian(self, librarian_id):
        librarian = self.db.fetch_query("SELECT * FROM librarians WHERE librarian_id = ?", (librarian_id,))
        return Librarian.from_db_row(librarian[0]) if librarian else None

    def add_librarian(self, name, librarian_id, email, password):
        self.db.execute_query(
            "INSERT INTO librarians (name, librarian_id, email, checkout_count, password) VALUES (?, ?, ?, 0, ?)",
            (name, librarian_id, email, password)
        )

    def delete_librarian(self, librarian_id):
        self.db.execute_query("DELETE FROM librarians WHERE librarian_id = ?", (librarian_id,))
