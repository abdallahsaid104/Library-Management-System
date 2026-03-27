from database import DatabaseManager


class LoanRepository:

    @staticmethod
    def create_loan(member_id, barcode, issue_date, due_date):
        db = DatabaseManager()
        db.execute_query(
            "INSERT INTO loans (member_id, book_barcode, issue_date, due_date) VALUES (?, ?, ?, ?)",
            (member_id, barcode, str(issue_date), str(due_date))
        )
        db.close()

    @staticmethod
    def get_active_loan(barcode):
        db = DatabaseManager()
        loan = db.fetch_query(
            "SELECT loan_id, due_date FROM loans WHERE book_barcode = ? AND return_date IS NULL",
            (barcode,)
        )
        db.close()
        return loan

    @staticmethod
    def get_active_loan_for_isbn(isbn):
        db = DatabaseManager()
        loans = db.fetch_query("""SELECT l.loan_id FROM loans l JOIN book_items bi ON l.book_barcode = bi.barcode
               WHERE bi.isbn = ? AND l.return_date IS NULL LIMIT 1""", (isbn,))
        db.close()
        return loans

    @staticmethod
    def get_active_loan_for_member(barcode, member_id):
        db = DatabaseManager()
        result = db.fetch_query(
            "SELECT loan_id, due_date FROM loans WHERE book_barcode = ? AND member_id = ? AND return_date IS NULL",
            (barcode, member_id)
        )
        db.close()
        return result

    @staticmethod
    def close_loan(loan_id, return_date, fine):
        db = DatabaseManager()
        db.execute_query(
            "UPDATE loans SET return_date = ?, fine_amount = ? WHERE loan_id = ?",
            (str(return_date), fine, loan_id)
        )
        db.close()

    @staticmethod
    def get_borrower_info(barcode):
        db = DatabaseManager()
        info = db.fetch_query("""
                SELECT m.name, m.member_id, m.email, l.due_date FROM loans l JOIN members m ON l.member_id = m.member_id
                WHERE l.book_barcode = ? AND l.return_date IS NULL""", (barcode,)
                              )
        db.close()
        return info

    @staticmethod
    def get_borrowed_books_by_member(member_id):
        db = DatabaseManager()
        books = db.fetch_query("""
                SELECT b.title, l.book_barcode, l.due_date  FROM loans l JOIN book_items bi ON l.book_barcode = bi.barcode
                JOIN books b ON bi.isbn = b.isbn WHERE l.member_id = ? AND l.return_date IS NULL""", (member_id,))
        db.close()
        return books

    @staticmethod
    def get_all_active_loans():
        db = DatabaseManager()
        loans = db.fetch_query("""SELECT m.name, m.member_id, b.title, l.book_barcode, l.due_date FROM loans l
                JOIN members m ON l.member_id = m.member_id JOIN book_items bi ON l.book_barcode = bi.barcode
                JOIN books b ON bi.isbn = b.isbn WHERE l.return_date IS NULL ORDER BY l.due_date ASC""")
        db.close()
        return loans

    @staticmethod
    def update_loan_due_date(loan_id, new_due_date):
        db = DatabaseManager()
        db.execute_query("UPDATE loans SET due_date = ? WHERE loan_id = ?", (str(new_due_date), loan_id))
        db.close()

    @staticmethod
    def get_overdue_loans(today):
        db = DatabaseManager()
        query = """SELECT l.member_id, l.book_barcode, l.due_date, b.title FROM loans l
                    JOIN book_items bi ON l.book_barcode = bi.barcode JOIN books b ON bi.isbn = b.isbn
                    WHERE l.return_date IS NULL AND l.due_date < ?"""
        loans = db.fetch_query(query, (str(today),))
        db.close()
        return loans
