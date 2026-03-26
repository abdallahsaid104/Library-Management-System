import sqlite3


class DatabaseManager:
    def __init__(self, db_name="library.db"):
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS books (isbn TEXT PRIMARY KEY, title TEXT NOT NULL,
                author TEXT NOT NULL, subject TEXT, publication_date TEXT)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS book_items (barcode TEXT PRIMARY KEY, isbn TEXT,
                rack_number TEXT, status TEXT DEFAULT 'available', FOREIGN KEY (isbn) REFERENCES books (isbn))""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS members (name TEXT NOT NULL, member_id TEXT PRIMARY KEY,
                        email TEXT, checkout_count INTEGER DEFAULT 0)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS loans (loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id TEXT, book_barcode TEXT, issue_date TEXT, due_date TEXT, return_date TEXT, 
                fine_amount REAL DEFAULT 0.0, FOREIGN KEY (member_id) REFERENCES members (member_id),
                FOREIGN KEY (book_barcode) REFERENCES book_items (barcode))""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS reservations (reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        member_id TEXT, isbn TEXT, reservation_date TEXT, status TEXT DEFAULT 'waiting',
                        FOREIGN KEY (member_id) REFERENCES members (member_id), FOREIGN KEY (isbn) REFERENCES books (isbn)
                        )""")

        self.connect.commit()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connect.commit()

    def fetch_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_dummy_data(self):
        self.cursor.execute("SELECT count(*) FROM books")
        if self.cursor.fetchone()[0] > 0:
            return

        books = [
            ("9780141439518", "Pride and Prejudice", "Jane Austen", "Classic literature", "2002-12-31"),
            ("9780735211292", "Atomic Habits", "James Clear", "Self-development", "2018-10-16"),
            ("9780743273565", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", "2004-09-30"),
            ("9780132350884", "Clean Code", "Robert C. Martin", "Programming", "2008-08-01"),
            ("9781612680194", "Rich Dad Poor Dad", "Robert T. Kiyosaki", "Personal finance", "2017-04-01")
        ]
        self.cursor.executemany("INSERT INTO books VALUES (?, ?, ?, ?, ?)", books)

        items = [
            ("B0001", "9780141439518", "A1", "available"),
            ("B0002", "9780141439518", "A1", "available"),
            ("B0003", "9780735211292", "B1", "available"),
            ("B0004", "9780735211292", "B1", "available"),
            ("B0005", "9780743273565", "C1", "available"),
            ("B0006", "9780743273565", "C1", "available"),
            ("B0007", "9780132350884", "D1", "available"),
            ("B0008", "9780132350884", "D1", "available"),
            ("B0009", "9781612680194", "E1", "available"),
            ("B0010", "9781612680194", "E1", "available")
        ]
        self.cursor.executemany("INSERT INTO book_items VALUES (?, ?, ?, ?)", items)

        members = [
            ("Abdallah said", "ID-MEM-001", "abdallah@gmail.com", 0),
            ("Eman said", "ID-MEM-002", "Eman@gmail.com", 0)
        ]
        self.cursor.executemany("INSERT INTO members VALUES (?, ?, ?, ?)", members)

        self.connect.commit()

        print("Library database initialized with dummy data")

    def close(self):
        self.connect.close()


