from database import DatabaseManager
from book import Book
from person import Member, Librarian
import time


def main():
    db = DatabaseManager()
    db.add_dummy_data()
    db.close()

    print("\nLibrary System Test")

    print("\nLibrarian Action")
    librarian = Librarian("Admin", "ID-EMP-001", "admin@getzew.com")
    librarian.add_book_item("B0020", "9780132350884", "D5")

    print("\nMember Checkout")
    member = Member.get_member("ID-MEM-001")

    if member:
        print(f"Member: {member.name} | Books Checked out: {member.checkout_count}")

        member.checkout_book("B0007")

        member.checkout_book("B9999")

        print("\nCurrently Borrowed Books")
        borrowed = Member.get_borrowed_books(member.id)
        for record in borrowed:
            print(f"Title: {record[0]}, Barcode: {record[1]}, Due: {record[2]}")

        print("\nReturn Book")
        member.return_book("B0007")

        print("\n--- Borrowed Books After Return ---")
        borrowed = Member.get_borrowed_books(member.id)
        if not borrowed:
            print("No books currently borrowed.")


if __name__ == '__main__':
    main()
