from database import DatabaseManager


class Book:
    def __init__(self, isbn, title, author, subject, publication_date):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.subject = subject
        self.publication_date = publication_date

    def __str__(self):
        info = f"""
Title:            {self.title}
Author:           {self.author}
Category:         {self.subject}
Publication Date: {self.publication_date}
"""
        return info

    @classmethod
    def search_books(cls, search_term, search_type="title"):
        query_map = {
            "title": "SELECT * FROM books WHERE title LIKE ?",
            "author": "SELECT * FROM books WHERE author LIKE ?",
            "subject": "SELECT * FROM books WHERE subject LIKE ?",
            "date": "SELECT * FROM books WHERE publication_date LIKE ?"
        }
        db = DatabaseManager()

        if search_type not in query_map:
            print("Invalid search type.")
            return []

        query = query_map[search_type]
        param = f"%{search_term}%"
        results = db.fetch_query(query, (param,))
        db.close()

        books = []
        for row in results:
            books.append(Book(row[0], row[1], row[2], row[3], row[4]))
        return books


class BookItem:
    def __init__(self, barcode, isbn, rack, status):
        self.barcode = barcode
        self.isbn = isbn
        self.rack = rack
        self.status = status

    @classmethod
    def get_available_copies(cls, isbn):
        db = DatabaseManager()
        query = "SELECT * FROM book_items WHERE isbn = ? AND status = 'available'"
        results = db.fetch_query(query, (isbn,))
        db.close()

        items = []
        for row in results:
            items.append(BookItem(row[0], row[1], row[2], row[3]))
        return items

