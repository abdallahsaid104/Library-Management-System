from database import DatabaseManager


class LibrarianRepository:

    @staticmethod
    def get_librarian(librarian_id):
        db = DatabaseManager()
        result = db.fetch_query("SELECT * FROM librarians WHERE librarian_id = ?", (librarian_id,))
        db.close()
        return result

    @staticmethod
    def add_librarian(name, librarian_id, email, password):
        db = DatabaseManager()
        db.execute_query(
            "INSERT INTO librarians (name, librarian_id, email, password) VALUES (?, ?, ?, ?)",
            (name, librarian_id, email, password)
        )
        db.close()

    @staticmethod
    def delete_librarian(librarian_id):
        db = DatabaseManager()
        db.execute_query("DELETE FROM librarians WHERE librarian_id = ?", (librarian_id,))
        db.close()