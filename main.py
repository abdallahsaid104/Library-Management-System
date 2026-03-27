from database import DatabaseManager
from person import Member
from book import Book
from services.librarian_service import LibrarianService
from services.member_service import MemberService
from services.notification_service import NotificationService


def run_demo():
    print("\n********************* Starting Automated Demo *********************")

    db = DatabaseManager()
    db.add_dummy_data()
    db.close()

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

    print("\n********************* Member Books Query *********************")
    if member2:
        MemberService.get_member_books(member2.id)

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

    print("\n********************* Demo Complete *********************")


def member_menu():
    while True:
        print("\n********************* MEMBER PORTAL *********************")
        print("1: Search for a Book")
        print("2: Check-out Book")
        print("3: Return Book")
        print("4: Reserve Book")
        print("5: Cancel Reservation")
        print("6: Renew Book")
        print("7: View My Checked-Out Books")
        print("8: Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == '1':
            term = input("Enter search term: ")
            results = Book.search_books(term)
            if results:
                for b in results:
                    print(f"- {b.title} by {b.author} (ISBN: {b.isbn})")
            else:
                print("No books found.")

        elif choice == '2':
            mid = input("Enter Member ID: ")
            barcode = input("Enter Book Barcode: ")
            member = Member.get_member(mid)
            if member:
                MemberService.checkout_book(member, barcode)
            else:
                print("Member not found.")

        elif choice == '3':
            mid = input("Enter Member ID: ")
            barcode = input("Enter Book Barcode: ")
            member = Member.get_member(mid)
            if member:
                MemberService.return_book(member, barcode)
            else:
                print("Member not found.")

        elif choice == '4':
            mid = input("Enter Member ID: ")
            isbn = input("Enter Book ISBN: ")
            member = Member.get_member(mid)
            if member:
                MemberService.reserve_book(member, isbn)
            else:
                print("Member not found.")

        elif choice == '5':
            mid = input("Enter Member ID: ")
            isbn = input("Enter Book ISBN: ")
            member = Member.get_member(mid)
            if member:
                MemberService.cancel_reservation(member, isbn)
            else:
                print("Member not found.")

        elif choice == '6':
            mid = input("Enter Member ID: ")
            barcode = input("Enter Book Barcode: ")
            member = Member.get_member(mid)
            if member:
                MemberService.renew_book(member, barcode)
            else:
                print("Member not found.")

        elif choice == '7':
            mid = input("Enter Member ID: ")
            MemberService.get_member_books(mid)

        elif choice == '8':
            break
        else:
            print("Invalid choice.")


def librarian_menu():
    while True:
        print("\n********************* LIBRARIAN PORTAL *********************")
        print("1: Add New Book (Catalog)")
        print("2: Add Book Item (Copy)")
        print("3: Remove Book Item")
        print("4: Remove Book (Title + Items)")
        print("5: Edit Book Details")
        print("6: Register New Member")
        print("7: Cancel Membership")
        print("8: View All Borrowed Books")
        print("9: Find Who Borrowed a Book")
        print("10: Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == '1':
            isbn = input("ISBN: ")
            title = input("Title: ")
            author = input("Author: ")
            subj = input("Subject: ")
            date = input("Pub Date (YYYY-MM-DD): ")
            LibrarianService.add_new_book(isbn, title, author, subj, date)

        elif choice == '2':
            barcode = input("Barcode: ")
            isbn = input("ISBN: ")
            rack = input("Rack: ")
            LibrarianService.add_book_item(barcode, isbn, rack)

        elif choice == '3':
            barcode = input("Barcode: ")
            LibrarianService.remove_book_item(barcode)

        elif choice == '4':
            isbn = input("ISBN: ")
            LibrarianService.remove_book(isbn)

        elif choice == '5':
            isbn = input("ISBN to edit: ")
            title = input("New Title (leave blank to skip): ")
            author = input("New Author (leave blank to skip): ")
            LibrarianService.edit_book(isbn, new_title=title or None, new_author=author or None)

        elif choice == '6':
            name = input("Name: ")
            mid = input("Member ID: ")
            email = input("Email: ")
            LibrarianService.register_member(name, mid, email)

        elif choice == '7':
            mid = input("Member ID: ")
            LibrarianService.cancel_membership(mid)

        elif choice == '8':
            LibrarianService.get_all_borrowed_books()

        elif choice == '9':
            barcode = input("Book Barcode: ")
            LibrarianService.get_book_borrower(barcode)

        elif choice == '10':
            break
        else:
            print("Invalid choice.")


def system_menu():
    print("\n********************* SYSTEM CHECKS *********************")
    print("Checking for overdue books...")
    NotificationService.check_overdue()
    input("\nPress Enter to return to main menu...")


def main():
    db = DatabaseManager()
    db.add_dummy_data()
    db.close()

    while True:
        print("\n********************* LIBRARY MANAGEMENT SYSTEM *********************")
        print("1. Run Demo (Test Scenario)")
        print("2. Enter Interactive Mode")
        print("3. Exit Application")

        choice = input("Select Option: ")

        if choice == '1':
            run_demo()
        elif choice == '2':
            while True:
                print("\n********************* Select Role *********************")
                print("1: Member Portal")
                print("2: Librarian Portal")
                print("3: System Checks")
                print("4: Back to Main Menu")
                role_choice = input("Select Role: ")

                if role_choice == '1':
                    member_menu()
                elif role_choice == '2':
                    librarian_menu()
                elif role_choice == '3':
                    system_menu()
                elif role_choice == '4':
                    break
                else:
                    print("Invalid selection")

        elif choice == '3':
            break
        else:
            print("Invalid selection")


if __name__ == '__main__':
    main()
