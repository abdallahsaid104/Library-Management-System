class LoanRepository:
    def __init__(self, db):
        self.db = db

    def create_loan(self, member_id, barcode, issue_date, due_date):
        self.db.execute_query(
            "INSERT INTO loans (member_id, book_barcode, issue_date, due_date) VALUES (?, ?, ?, ?)",
            (member_id, barcode, str(issue_date), str(due_date))
        )

    def get_active_loan(self, barcode):
        return self.db.fetch_query(
            "SELECT loan_id, due_date FROM loans WHERE book_barcode = ? AND return_date IS NULL",
            (barcode,)
        )

    def get_active_loan_for_isbn(self, isbn):
        return self.db.fetch_query(
            """SELECT l.loan_id FROM loans l JOIN book_items bi ON l.book_barcode = bi.barcode
               WHERE bi.isbn = ? AND l.return_date IS NULL LIMIT 1""", (isbn,))

    def get_active_loan_for_member(self, barcode, member_id):
        return self.db.fetch_query(
            "SELECT loan_id, due_date FROM loans WHERE book_barcode = ? AND member_id = ? AND return_date IS NULL",
            (barcode, member_id)
        )

    def close_loan(self, loan_id, return_date, fine):
        self.db.execute_query(
            "UPDATE loans SET return_date = ?, fine_amount = ? WHERE loan_id = ?",
            (str(return_date), fine, loan_id)
        )

    def get_borrower_info(self, barcode):
        return self.db.fetch_query(
            """SELECT m.name, m.member_id, m.email, l.due_date FROM loans l 
            JOIN members m ON l.member_id = m.member_id WHERE l.book_barcode = ? AND l.return_date IS NULL""",
            (barcode,)
        )

    def get_borrowed_books_by_member(self, member_id):
        return self.db.fetch_query(
            """SELECT b.title, l.book_barcode, l.due_date  FROM loans l 
            JOIN book_items bi ON l.book_barcode = bi.barcode JOIN books b ON bi.isbn = b.isbn 
            WHERE l.member_id = ? AND l.return_date IS NULL""", (member_id,))

    def get_all_active_loans(self):
        return self.db.fetch_query(
            """SELECT m.name, m.member_id, b.title, l.book_barcode, l.due_date FROM loans l
            JOIN members m ON l.member_id = m.member_id JOIN book_items bi ON l.book_barcode = bi.barcode
            JOIN books b ON bi.isbn = b.isbn WHERE l.return_date IS NULL ORDER BY l.due_date ASC""")

    def update_loan_due_date(self, loan_id, new_due_date):
        self.db.execute_query("UPDATE loans SET due_date = ? WHERE loan_id = ?", (str(new_due_date), loan_id))

    def get_overdue_loans(self, today):
        return self.db.fetch_query(
            """SELECT l.member_id, l.book_barcode, l.due_date, b.title FROM loans l
            JOIN book_items bi ON l.book_barcode = bi.barcode JOIN books b ON bi.isbn = b.isbn
            WHERE l.return_date IS NULL AND l.due_date < ?""", (str(today),))