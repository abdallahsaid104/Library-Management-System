class Book:
    def __init__(self, isbn, title, author, subject, publication_date):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.subject = subject
        self.publication_date = publication_date

    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nCategory: {self.subject}\nPublication Date: {self.publication_date}"

    @classmethod
    def from_db_row(cls, row):
        return cls(row[0], row[1], row[2], row[3], row[4])


class BookItem:
    def __init__(self, barcode, isbn, rack, status):
        self.barcode = barcode
        self.isbn = isbn
        self.rack = rack
        self.status = status

    def __str__(self):
        return f"Barcode: {self.barcode} | ISBN: {self.isbn} | Rack: {self.rack} | Status: {self.status}"

    @classmethod
    def from_db_row(cls, row):
        return cls(row[0], row[1], row[2], row[3])

