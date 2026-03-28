class LibrarianRepository:

    def __init__(self, db):
        self.db = db

    def get_librarian(self, librarian_id):
        return self.db.fetch_query("SELECT * FROM librarians WHERE librarian_id = ?", (librarian_id,))

    def add_librarian(self, name, librarian_id, email, password):
        self.db.execute_query("INSERT INTO librarians (name, librarian_id, email, password) VALUES (?, ?, ?, ?)",
                              (name, librarian_id, email, password)
                              )

    def delete_librarian(self, librarian_id):
        self.db.execute_query("DELETE FROM librarians WHERE librarian_id = ?", (librarian_id,))
