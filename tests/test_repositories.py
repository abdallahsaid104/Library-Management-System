import pytest
from unittest.mock import patch, MagicMock
from repositories.librarian_repository import LibrarianRepository
from repositories.loan_repository import LoanRepository
from repositories.member_repository import MemberRepository
from repositories.book_repository import BookRepository


def test_get_librarian():
    db = MagicMock()
    db.fetch_query.return_value = [("zezo", "LIB-001", "zezo@lib.com", "zoz123")]

    repo = LibrarianRepository(db)
    librarian = repo.get_librarian("LIB-001")

    assert librarian == [("zezo", "LIB-001", "zezo@lib.com", "zoz123")]

    db.fetch_query.assert_called_with("SELECT * FROM librarians WHERE librarian_id = ?", ("LIB-001",))


def test_add_librarian():
    db = MagicMock()
    repo = LibrarianRepository(db)
    repo.add_librarian("sabry", "LIB-002", "sabry@lib.com", "sabry123")

    db.execute_query.assert_called_with(
        "INSERT INTO librarians (name, librarian_id, email, password) VALUES (?, ?, ?, ?)",
        ("sabry", "LIB-002", "sabry@lib.com", "sabry123")
    )


def test_delete_librarian():
    db = MagicMock()
    repo = LibrarianRepository(db)
    repo.delete_librarian("LIB-002")

    db.execute_query.assert_called_with("DELETE FROM librarians WHERE librarian_id = ?", ("LIB-002",))


def test_create_loan():
    db = MagicMock()
    repo = LoanRepository(db)
    repo.create_loan("MEM-001", "B0001", "2023-10-01", "2023-10-11")

    db.execute_query.assert_called_with(
        "INSERT INTO loans (member_id, book_barcode, issue_date, due_date) VALUES (?, ?, ?, ?)",
        ("MEM-001", "B0001", "2023-10-01", "2023-10-11")
    )


def test_get_active_loan():
    db = MagicMock()
    db.fetch_query.return_value = [(1, "2023-10-11")]
    repo = LoanRepository(db)

    loan = repo.get_active_loan("B0001")

    assert loan == [(1, "2023-10-11")]
    db.fetch_query.assert_called_with(
        "SELECT loan_id, due_date FROM loans WHERE book_barcode = ? AND return_date IS NULL",
        ("B0001",)
    )


def test_get_active_loan_for_isbn():
    db = MagicMock()
    repo = LoanRepository(db)
    repo.get_active_loan_for_isbn("999-999")

    db.fetch_query.assert_called_with(
        """SELECT l.loan_id FROM loans l JOIN book_items bi ON l.book_barcode = bi.barcode
               WHERE bi.isbn = ? AND l.return_date IS NULL LIMIT 1""", ("999-999",)
    )


def test_get_active_loan_for_member():
    db = MagicMock()
    repo = LoanRepository(db)
    repo.get_active_loan_for_member("B0001", "MEM-001")

    db.fetch_query.assert_called_with(
        "SELECT loan_id, due_date FROM loans WHERE book_barcode = ? AND member_id = ? AND return_date IS NULL",
        ("B0001", "MEM-001")
    )


def test_close_loan():
    db = MagicMock()
    repo = LoanRepository(db)
    repo.close_loan(1, "2023-10-05", 50.0)

    db.execute_query.assert_called_with(
        "UPDATE loans SET return_date = ?, fine_amount = ? WHERE loan_id = ?",
        ("2023-10-05", 50.0, 1)
    )


def test_get_borrower_info():
    db = MagicMock()
    repo = LoanRepository(db)
    repo.get_borrower_info("B0001")

    db.fetch_query.assert_called_with("""SELECT m.name, m.member_id, m.email, l.due_date FROM loans l 
        JOIN members m ON l.member_id = m.member_id WHERE l.book_barcode = ? AND l.return_date IS NULL""", ("B0001",))


def test_get_borrowed_books_by_member():
    db = MagicMock()
    repo = LoanRepository(db)
    repo.get_borrowed_books_by_member("MEM-001")

    db.fetch_query.assert_called_with("""SELECT b.title, l.book_barcode, l.due_date  FROM loans l 
        JOIN book_items bi ON l.book_barcode = bi.barcode JOIN books b ON bi.isbn = b.isbn 
        WHERE l.member_id = ? AND l.return_date IS NULL""", ("MEM-001",))


def test_get_all_active_loans():
    db = MagicMock()
    repo = LoanRepository(db)
    repo.get_all_active_loans()

    db.fetch_query.assert_called_with(
        """SELECT m.name, m.member_id, b.title, l.book_barcode, l.due_date FROM loans l
                JOIN members m ON l.member_id = m.member_id JOIN book_items bi ON l.book_barcode = bi.barcode
                JOIN books b ON bi.isbn = b.isbn WHERE l.return_date IS NULL ORDER BY l.due_date ASC"""
    )


def test_update_loan_due_date():
    db = MagicMock()
    repo = LoanRepository(db)
    repo.update_loan_due_date(1, "2023-10-20")

    db.execute_query.assert_called_with(
        "UPDATE loans SET due_date = ? WHERE loan_id = ?", ("2023-10-20", 1)
    )


def test_get_overdue_loans():
    db = MagicMock()
    repo = LoanRepository(db)
    repo.get_overdue_loans("2023-10-15")

    db.fetch_query.assert_called_with(
        """SELECT l.member_id, l.book_barcode, l.due_date, b.title FROM loans l
                    JOIN book_items bi ON l.book_barcode = bi.barcode JOIN books b ON bi.isbn = b.isbn
                    WHERE l.return_date IS NULL AND l.due_date < ?""", ("2023-10-15",))


def test_get_member():
    db = MagicMock()
    db.fetch_query.return_value = [("Ahmed", "MEM-001", "ahmed@email.com", 0, "1234")]
    repo = MemberRepository(db)

    member = repo.get_member("MEM-001")

    assert member == [("Ahmed", "MEM-001", "ahmed@email.com", 0, "1234")]
    db.fetch_query.assert_called_with("SELECT * FROM members WHERE member_id = ?", ("MEM-001",))


def test_update_checkout_count_increment():
    db = MagicMock()
    repo = MemberRepository(db)
    repo.update_checkout_count("MEM-001", increment=True)

    args, kwargs = db.execute_query.call_args
    assert "checkout_count = checkout_count + 1" in args[0]
    assert args[1] == ("MEM-001",)


def test_update_checkout_count_decrement():
    db = MagicMock()
    repo = MemberRepository(db)
    repo.update_checkout_count("MEM-001", increment=False)

    args, kwargs = db.execute_query.call_args
    assert "checkout_count = checkout_count - 1" in args[0]
    assert args[1] == ("MEM-001",)


def test_add_reservation():
    db = MagicMock()
    repo = MemberRepository(db)
    repo.add_reservation("MEM-001", "999-999", "2023-10-01")

    db.execute_query.assert_called_with(
        "INSERT INTO reservations (member_id, isbn, reservation_date) VALUES (?, ?, ?)",
        ("MEM-001", "999-999", "2023-10-01")
    )


def test_get_waiting_reservation():
    db = MagicMock()
    repo = MemberRepository(db)
    repo.get_waiting_reservation("999-999")

    db.fetch_query.assert_called_with(
        "SELECT member_id FROM reservations WHERE isbn = ? AND status = 'waiting' LIMIT 1",
        ("999-999",)
    )


def test_get_reservation():
    db = MagicMock()
    repo = MemberRepository(db)
    repo.get_reservation("MEM-001", "999-999")

    db.fetch_query.assert_called_with(
        "SELECT * FROM reservations WHERE member_id = ? AND isbn = ? AND status = 'waiting'",
        ("MEM-001", "999-999")
    )


def test_update_reservation_status():
    db = MagicMock()
    repo = MemberRepository(db)
    repo.update_reservation_status("MEM-001", "999-999", "notified")

    db.execute_query.assert_called_with(
        "UPDATE reservations SET status = ? WHERE member_id = ? AND isbn = ?",
        ("notified", "MEM-001", "999-999")
    )


def test_cancel_reservation():
    db = MagicMock()
    repo = MemberRepository(db)
    repo.cancel_reservation("MEM-001", "999-999")

    db.execute_query.assert_called_with(
        "DELETE FROM reservations WHERE member_id = ? AND isbn = ? AND status = 'waiting'",
        ("MEM-001", "999-999")
    )


def test_add_member():
    db = MagicMock()
    repo = MemberRepository(db)
    repo.add_member("Ali", "MEM-005", "ali@email.com", "ali123")

    db.execute_query.assert_called_with(
        "INSERT INTO members (name, member_id, email, checkout_count, password) VALUES (?, ?, ?, 0, ?)",
        ("Ali", "MEM-005", "ali@email.com", "ali123")
    )


def test_delete_member():
    db = MagicMock()
    repo = MemberRepository(db)
    repo.delete_member("MEM-005")

    db.execute_query.assert_called_with("DELETE FROM members WHERE member_id = ?", ("MEM-005",))


def test_search_books():
    db = MagicMock()
    repo = BookRepository(db)
    repo.search_books("Gatsby", "title")

    db.fetch_query.assert_called_with(
        "SELECT * FROM books WHERE title LIKE ?", ("%Gatsby%",)
    )


def test_get_book_item():
    db = MagicMock()
    db.fetch_query.return_value = [("B0001", "999-999", "A1", "available")]
    repo = BookRepository(db)

    item = repo.get_book_item("B0001")

    assert item == [("B0001", "999-999", "A1", "available")]
    db.fetch_query.assert_called_with("SELECT * FROM book_items WHERE barcode = ?", ("B0001",))


def test_update_item_status():
    db = MagicMock()
    repo = BookRepository(db)
    repo.update_item_status("B0001", "loaned")

    db.execute_query.assert_called_with(
        "UPDATE book_items SET status = ? WHERE barcode = ?", ("loaned", "B0001")
    )


def test_get_book_by_isbn():
    db = MagicMock()
    repo = BookRepository(db)
    repo.get_book_by_isbn("999-999")

    db.fetch_query.assert_called_with("SELECT * FROM books WHERE isbn = ?", ("999-999",))


def test_get_items_by_isbn():
    db = MagicMock()
    repo = BookRepository(db)
    repo.get_items_by_isbn("999-999")

    db.fetch_query.assert_called_with("SELECT * FROM book_items WHERE isbn = ?", ("999-999",))


def test_add_book():
    db = MagicMock()
    repo = BookRepository(db)
    repo.add_book("999-999", "Test Book", "Author X", "Sci-Fi", "2023-01-01")

    db.execute_query.assert_called_with(
        "INSERT INTO books VALUES (?, ?, ?, ?, ?)",
        ("999-999", "Test Book", "Author X", "Sci-Fi", "2023-01-01")
    )


def test_update_book():
    db = MagicMock()
    repo = BookRepository(db)
    repo.update_book("999-999", title="New Title", author="New Author", subject="Fantasy")

    args, kwargs = db.execute_query.call_args
    assert "UPDATE books SET" in args[0]
    assert "title = ?" in args[0]
    assert "author = ?" in args[0]
    assert "subject = ?" in args[0]
    assert args[1] == ("New Title", "New Author", "Fantasy", "999-999")


def test_remove_book():
    db = MagicMock()
    repo = BookRepository(db)
    repo.remove_book("999-999")

    db.execute_query.assert_called_with("DELETE FROM books WHERE isbn = ?", ("999-999",))


def test_add_book_item():
    db = MagicMock()
    repo = BookRepository(db)
    repo.add_book_item("B0099", "999-999", "Z1")

    db.execute_query.assert_called_with(
        "INSERT INTO book_items (barcode, isbn, rack_number, status) VALUES (?, ?, ?, 'available')",
        ("B0099", "999-999", "Z1")
    )


def test_remove_book_item():
    db = MagicMock()
    repo = BookRepository(db)
    repo.remove_book_item("B0099")

    db.execute_query.assert_called_with("DELETE FROM book_items WHERE barcode = ?", ("B0099",))


def test_remove_items_by_isbn():
    db = MagicMock()
    repo = BookRepository(db)
    repo.remove_items_by_isbn("999-999")

    db.execute_query.assert_called_with("DELETE FROM book_items WHERE isbn = ?", ("999-999",))


def test_update_book_item():
    db = MagicMock()
    repo = BookRepository(db)
    repo.update_book_item("B0099", rack="A5", status="damaged")

    args, kwargs = db.execute_query.call_args
    assert "UPDATE book_items SET" in args[0]
    assert "rack = ?" in args[0]
    assert "status = ?" in args[0]
    assert args[1] == ("A5", "damaged", "B0099")
