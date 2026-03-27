from database import DatabaseManager
from book import Book
from person import Member, Librarian
from services.librarian_service import LibrarianService
from services.member_service import MemberService
from services.notification_service import NotificationService


def main():
    db = DatabaseManager()
    db.add_dummy_data()
    db.close()

    print("\n********************* Library System Test *********************")

    print("\n********************* ADD Book Phase *********************")
    LibrarianService.add_book_item("B0020", "9780132350884", "D5")

    print("\n********************* Checkout Phase *********************")
    member1 = Member.get_member("ID-MEM-001")
    if member1:
        MemberService.checkout_book(member1, "B0007")

    print("\n********************* Reservation Phase *********************")
    member2 = Member.get_member("ID-MEM-002")
    if member2:
        MemberService.checkout_book(member2, "B0007")
        MemberService.reserve_book(member2, "9780132350884")

    print("\n********************* Librarian Report Phase *********************")
    LibrarianService.get_all_borrowed_books()

    print("\n********************* Renewal Logic Test *********************")
    if member1:
        MemberService.renew_book(member1, "B0007")

    print("\n********************* Return & Notification Phase *********************")
    if member1:
        MemberService.return_book(member1, "B0007")

    print("\n********************* Query Specific Book *********************")
    if member2:
        MemberService.checkout_book(member2, "B0007")

    LibrarianService.get_book_borrower("B0007")

    print("\n********************* System Overdue Check *********************")
    NotificationService.check_overdue()

    print("\n********************* Management Phase *********************")

    LibrarianService.add_new_book("999-999", "The Future of AI", "Tech Author", "Technology", "2025-01-01")
    LibrarianService.edit_book("999-999", new_title="The Future of AI (2nd Edition)")

    LibrarianService.cancel_membership("ID-MEM-002")

    if member1:
        MemberService.reserve_book(member1, "9780735211292")
        MemberService.cancel_reservation(member1, "9780735211292")

    LibrarianService.remove_book_item("B0020")

    LibrarianService.remove_book("999-999")

    print("\n********************* Test Complete *********************")


if __name__ == '__main__':
    main()
