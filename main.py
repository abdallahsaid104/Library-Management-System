from database import DatabaseManager
from book import Book
from person import Member, Librarian


def main():
    db = DatabaseManager()
    db.add_dummy_data()
    db.close()

    print("Library system test")

    print("Test Librarian")
    librarian = Librarian("Admin", "ID-EMP-001", "admin@getzew.com")
    print(librarian)

    librarian.add_book_item("B0011", "9780132350884", "D1")

    print("\nTest Member")
    member = Member.get_member("ID-MEM-001")
    if member:
        print(member)
        print(f"Can checkout? {member.can_checkout()}")

    print("\nBook Search")
    search_result = Book.search_books("Clean Code", "title")
    for result in search_result:
        print(result)


if __name__ == '__main__':
    main()

