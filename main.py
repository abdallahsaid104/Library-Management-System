from database import DatabaseManager
from book import Book
from person import Member, Librarian


def main():
    db = DatabaseManager()
    db.add_dummy_data()
    db.close()

    print("\n********************* Library System Test *********************")

    print("\n********************* Checkout Phase *********************")
    member1 = Member.get_member("ID-MEM-001")
    member1.checkout_book("B0007")

    print("\n********************* Reservation Phase *********************")
    member2 = Member.get_member("ID-MEM-002")
    member2.checkout_book("B0007")

    member2.reserve_book("9780132350884")

    print("\n********************* Return & Notification Phase *********************")
    member1.return_book("B0007")


if __name__ == '__main__':
    main()
