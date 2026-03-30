import os
import io
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from services.librarian_service import LibrarianService
from services.member_service import MemberService
from services.notification_service import NotificationService
from UI.styles import (MAIN_STYLE, BUTTON_PRIMARY, LABEL_TITLE, LABEL_ERROR,
                       LABEL_SUCCESS, LABEL_SECTION, LABEL_AVATAR,
                       LABEL_MEMBER_NAME, LABEL_BADGE_LIBRARIAN, WIDGET_SIDEBAR,
                       BUTTON_SIGN_OUT)

UI_PATH = os.path.join(os.path.dirname(__file__), "", "librarian_portal.ui")


class LibrarianWindow(QMainWindow):
    def __init__(self, librarian, login_window):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.librarian = librarian
        self.login_window = login_window

        self._apply_styles()
        self._setup_profile()
        self._connect_nav()
        self.current_page = "add_book"
        self._show_add_book()

    def _apply_styles(self):
        self.setStyleSheet(MAIN_STYLE)
        self.widget_sidebar.setStyleSheet(WIDGET_SIDEBAR)
        self.label_page_title.setStyleSheet(LABEL_TITLE)
        self.label_avatar.setStyleSheet(LABEL_AVATAR)
        self.label_librarian_name.setStyleSheet(LABEL_MEMBER_NAME)
        self.label_librarian_badge.setStyleSheet(LABEL_BADGE_LIBRARIAN)
        self.label_section_catalog.setStyleSheet(LABEL_SECTION)
        self.label_section_members.setStyleSheet(LABEL_SECTION)
        self.label_section_loans.setStyleSheet(LABEL_SECTION)
        self.label_section_my_account.setStyleSheet(LABEL_SECTION)
        self.label_section_admin.setStyleSheet(LABEL_SECTION)
        self.label_result_msg.setStyleSheet(LABEL_ERROR)
        self.button_action.setStyleSheet(BUTTON_PRIMARY)
        self.button_secondary.setStyleSheet(
            "background-color:transparent;border:1px solid #3a3f4e;border-radius:6px;"
            "color:#ffffff;font-size:13px;min-height:36px;padding:6px 16px;"
        )
        self.button_sign_out.setStyleSheet(BUTTON_SIGN_OUT)

    def _setup_profile(self):
        initials = "".join(w[0].upper() for w in self.librarian.name.split()[:2])
        self.label_avatar.setText(initials)
        self.label_librarian_name.setText(self.librarian.name)

    def _connect_nav(self):
        self.nav_buttons = [
            self.button_add_book, self.button_add_copy,
            self.button_register_member, self.button_cancel_membership,
            self.button_all_loans, self.button_find_borrower,
            self.button_search, self.button_my_checkout, self.button_my_return,
            self.button_my_renew, self.button_my_reserve, self.button_my_cancel_res,
            self.button_my_books,
            self.button_register_librarian, self.button_overdue
        ]
        self.button_add_book.clicked.connect(self._show_add_book)
        self.button_add_copy.clicked.connect(self._show_add_copy)
        self.button_register_member.clicked.connect(self._show_register_member)
        self.button_cancel_membership.clicked.connect(self._show_cancel_membership)
        self.button_all_loans.clicked.connect(self._show_all_loans)
        self.button_find_borrower.clicked.connect(self._show_find_borrower)

        self.button_search.clicked.connect(self._show_search)
        self.button_my_checkout.clicked.connect(self._show_checkout)
        self.button_my_return.clicked.connect(self._show_return)
        self.button_my_renew.clicked.connect(self._show_renew)
        self.button_my_reserve.clicked.connect(self._show_reserve)
        self.button_my_cancel_res.clicked.connect(self._show_cancel_reservation)
        self.button_my_books.clicked.connect(self._show_my_books)

        self.button_register_librarian.clicked.connect(self._show_register_librarian)
        self.button_overdue.clicked.connect(self._show_overdue)
        self.button_sign_out.clicked.connect(self._sign_out)
        self.button_action.clicked.connect(self._handle_action)
        self.button_secondary.clicked.connect(self._handle_secondary)

    def _set_active_nav(self, active):
        for btn in self.nav_buttons:
            btn.setChecked(btn == active)

    def _clear_content(self):
        for field in [self.lineEdit_isbn, self.lineEdit_title, self.lineEdit_author,
                      self.lineEdit_subject, self.lineEdit_pub_date]:
            field.setVisible(False)
            field.clear()

        self.comboBox_search_type.setVisible(False)
        self.lineEdit_search_input.setVisible(False)
        self.lineEdit_search_input.clear()

        self.tableWidget_results.setVisible(False)
        self.label_result_msg.setText("")
        self.button_action.setVisible(True)
        self.button_secondary.setVisible(False)

    def _show_add_book(self):
        self._clear_content()
        self._set_active_nav(self.button_add_book)
        self.current_page = "add_book"
        self.label_page_title.setText("Add / edit book")
        for f in [self.lineEdit_isbn, self.lineEdit_title,
                  self.lineEdit_author, self.lineEdit_subject, self.lineEdit_pub_date]:
            f.setVisible(True)
        self.lineEdit_isbn.setPlaceholderText("ISBN")
        self.lineEdit_title.setPlaceholderText("Title")
        self.lineEdit_author.setPlaceholderText("Author")
        self.lineEdit_subject.setPlaceholderText("Subject")
        self.lineEdit_pub_date.setPlaceholderText("Publication date (YYYY-MM-DD)")
        self.button_action.setText("Add book")
        self.button_secondary.setVisible(True)
        self.button_secondary.setText("Edit book")

    def _show_add_copy(self):
        self._clear_content()
        self._set_active_nav(self.button_add_copy)
        self.current_page = "add_copy"
        self.label_page_title.setText("Add / remove copy")
        for f in [self.lineEdit_isbn, self.lineEdit_title, self.lineEdit_author]:
            f.setVisible(True)
        self.lineEdit_isbn.setPlaceholderText("ISBN")
        self.lineEdit_title.setPlaceholderText("Barcode")
        self.lineEdit_author.setPlaceholderText("Rack number")
        self.button_action.setText("Add copy")
        self.button_secondary.setVisible(True)
        self.button_secondary.setText("Remove copy")

    def _show_register_member(self):
        self._clear_content()
        self._set_active_nav(self.button_register_member)
        self.current_page = "register_member"
        self.label_page_title.setText("Register member")
        for f in [self.lineEdit_isbn, self.lineEdit_title,
                  self.lineEdit_author, self.lineEdit_subject]:
            f.setVisible(True)
        self.lineEdit_isbn.setPlaceholderText("Member ID")
        self.lineEdit_title.setPlaceholderText("Full name")
        self.lineEdit_author.setPlaceholderText("Email")
        self.lineEdit_subject.setPlaceholderText("Password (default: 1234)")
        self.button_action.setText("Register member")

    def _show_cancel_membership(self):
        self._clear_content()
        self._set_active_nav(self.button_cancel_membership)
        self.current_page = "cancel_membership"
        self.label_page_title.setText("Cancel membership")
        self.lineEdit_isbn.setVisible(True)
        self.lineEdit_isbn.setPlaceholderText("Member ID")
        self.button_action.setText("Cancel membership")

    def _show_all_loans(self):
        self._clear_content()
        self._set_active_nav(self.button_all_loans)
        self.current_page = "all_loans"
        self.label_page_title.setText("All borrowed books")
        self.button_action.setVisible(False)
        self.tableWidget_results.setVisible(True)
        self._setup_table(["Member", "Member ID", "Title", "Barcode", "Due Date"])
        self._load_all_loans()

    def _show_find_borrower(self):
        self._clear_content()
        self._set_active_nav(self.button_find_borrower)
        self.current_page = "find_borrower"
        self.label_page_title.setText("Find who borrowed a book")
        self.lineEdit_isbn.setVisible(True)
        self.lineEdit_isbn.setPlaceholderText("Enter book barcode...")
        self.button_action.setText("Search")

    def _show_register_librarian(self):
        self._clear_content()
        self._set_active_nav(self.button_register_librarian)
        self.current_page = "register_librarian"
        self.label_page_title.setText("Register new librarian")
        for f in [self.lineEdit_isbn, self.lineEdit_title,
                  self.lineEdit_author, self.lineEdit_subject]:
            f.setVisible(True)
        self.lineEdit_isbn.setPlaceholderText("Librarian ID")
        self.lineEdit_title.setPlaceholderText("Full name")
        self.lineEdit_author.setPlaceholderText("Email")
        self.lineEdit_subject.setPlaceholderText("Password")
        self.button_action.setText("Register librarian")

    def _show_overdue(self):
        self._clear_content()
        self._set_active_nav(self.button_overdue)
        self.current_page = "overdue"
        self.label_page_title.setText("System overdue check")
        self.button_action.setText("Run overdue check")

    def _show_search(self):
        self._clear_content()
        self._set_active_nav(self.button_search)
        self.current_page = "search"
        self.label_page_title.setText("Search catalog")
        self.comboBox_search_type.setVisible(True)
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter search term...")
        self.button_action.setText("Search")
        self.button_secondary.setVisible(False)
        self.tableWidget_results.setVisible(True)
        self._setup_table(["Title", "Author", "Subject", "ISBN"])

    def _show_checkout(self):
        self._clear_content()
        self._set_active_nav(self.button_my_checkout)
        self.current_page = "checkout"
        self.label_page_title.setText("Check out book")
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter book barcode...")
        self.button_action.setText("Check out")

    def _show_return(self):
        self._clear_content()
        self._set_active_nav(self.button_my_return)
        self.current_page = "return"
        self.label_page_title.setText("Return book")
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter book barcode...")
        self.button_action.setText("Return book")

    def _show_renew(self):
        self._clear_content()
        self._set_active_nav(self.button_my_renew)
        self.current_page = "renew"
        self.label_page_title.setText("Renew book")
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter book barcode...")
        self.button_action.setText("Renew")

    def _show_reserve(self):
        self._clear_content()
        self._set_active_nav(self.button_my_reserve)
        self.current_page = "reserve"
        self.label_page_title.setText("Reserve book")
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter book ISBN...")
        self.button_action.setText("Reserve")

    def _show_cancel_reservation(self):
        self._clear_content()
        self._set_active_nav(self.button_my_cancel_res)
        self.current_page = "cancel_res"
        self.label_page_title.setText("Cancel reservation")
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter book ISBN...")
        self.button_action.setText("Cancel reservation")

    def _show_my_books(self):
        self._clear_content()
        self._set_active_nav(self.button_my_books)
        self.current_page = "my_books"
        self.label_page_title.setText("My checked-out books")
        self.button_action.setVisible(False)
        self.tableWidget_results.setVisible(True)
        self._setup_table(["Title", "Barcode", "Due Date"])
        self._load_my_books()

    def _setup_table(self, headers):
        self.tableWidget_results.setColumnCount(len(headers))
        self.tableWidget_results.setHorizontalHeaderLabels(headers)
        self.tableWidget_results.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_results.setRowCount(0)

    def _capture(self, func, *args, **kwargs):
        captured = io.StringIO()
        sys.stdout = captured
        func(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return captured.getvalue().strip()

    def _show_msg(self, msg, success=True):
        self.label_result_msg.setStyleSheet(LABEL_SUCCESS if success else LABEL_ERROR)
        self.label_result_msg.setText(msg)

    def _handle_action(self):
        action_map = {
            "add_book": self._do_add_book,
            "add_copy": self._do_add_copy,
            "register_member": self._do_register_member,
            "cancel_membership": self._do_cancel_membership,
            "find_borrower": self._do_find_borrower,
            "register_librarian": self._do_register_librarian,
            "overdue": self._do_overdue,
            "search": self._do_search,
            "checkout": self._do_checkout,
            "return": self._do_return,
            "renew": self._do_renew,
            "reserve": self._do_reserve,
            "cancel_res": self._do_cancel_reservation
        }
        if self.current_page in action_map:
            action_map[self.current_page]()

    def _handle_secondary(self):
        secondary_map = {
            "add_book": self._do_edit_book,
            "add_copy": self._do_remove_copy
        }
        if self.current_page in secondary_map:
            secondary_map[self.current_page]()

    def _do_add_book(self):
        msg = self._capture(LibrarianService.add_new_book,
                            self.lineEdit_isbn.text().strip(), self.lineEdit_title.text().strip(),
                            self.lineEdit_author.text().strip(), self.lineEdit_subject.text().strip(),
                            self.lineEdit_pub_date.text().strip())
        self._show_msg(msg, success="Success" in msg)

    def _do_edit_book(self):
        msg = self._capture(LibrarianService.edit_book,
                            self.lineEdit_isbn.text().strip(),
                            self.lineEdit_title.text().strip() or None,
                            self.lineEdit_author.text().strip() or None,
                            self.lineEdit_subject.text().strip() or None)
        self._show_msg(msg, success="Success" in msg)

    def _do_add_copy(self):
        msg = self._capture(LibrarianService.add_book_item,
                            self.lineEdit_title.text().strip(),
                            self.lineEdit_isbn.text().strip(),
                            self.lineEdit_author.text().strip())
        self._show_msg(msg, success="Success" in msg)

    def _do_remove_copy(self):
        msg = self._capture(LibrarianService.remove_book_item,
                            self.lineEdit_title.text().strip())
        self._show_msg(msg, success="Success" in msg)

    def _do_register_member(self):
        password = self.lineEdit_subject.text().strip() or "1234"
        msg = self._capture(LibrarianService.register_member,
                            self.lineEdit_title.text().strip(),
                            self.lineEdit_isbn.text().strip(),
                            self.lineEdit_author.text().strip(), password)
        self._show_msg(msg, success="Success" in msg)

    def _do_cancel_membership(self):
        msg = self._capture(LibrarianService.cancel_membership,
                            self.lineEdit_isbn.text().strip())
        self._show_msg(msg, success="Success" in msg)

    def _do_find_borrower(self):
        msg = self._capture(LibrarianService.get_book_borrower,
                            self.lineEdit_isbn.text().strip())
        self._show_msg(msg, success="currently borrowed" in msg)

    def _do_register_librarian(self):
        msg = self._capture(LibrarianService.register_librarian,
                            self.lineEdit_title.text().strip(),
                            self.lineEdit_isbn.text().strip(),
                            self.lineEdit_author.text().strip(),
                            self.lineEdit_subject.text().strip())
        self._show_msg(msg, success="Success" in msg)

    def _do_overdue(self):
        msg = self._capture(NotificationService.check_overdue)
        self._show_msg(msg, success="No overdue" in msg)

    def _do_search(self):
        term = self.lineEdit_search_input.text().strip()
        if not term:
            self._show_msg("Please enter a search term.", success=False)
            return
        type_map = {0: "title", 1: "author", 2: "subject", 3: "date"}
        search_type = type_map[self.comboBox_search_type.currentIndex()]
        results = MemberService.search_books(term, search_type)
        self.tableWidget_results.setRowCount(0)
        if not results:
            self._show_msg("No books found.", success=False)
            return
        for row_idx, book in enumerate(results):
            self.tableWidget_results.insertRow(row_idx)
            for col_idx, val in enumerate([book.title, book.author, book.subject, book.isbn]):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget_results.setItem(row_idx, col_idx, item)
        self._show_msg(f"{len(results)} result(s) found.")

    def _do_checkout(self):
        barcode = self.lineEdit_search_input.text().strip()
        if not barcode:
            self._show_msg("Please enter a barcode.", success=False)
            return
        msg = self._capture(MemberService.checkout_book, self.librarian, barcode)
        self._show_msg(msg, success="Success" in msg)

    def _do_return(self):
        barcode = self.lineEdit_search_input.text().strip()
        if not barcode:
            self._show_msg("Please enter a barcode.", success=False)
            return
        msg = self._capture(MemberService.return_book, self.librarian, barcode)
        self._show_msg(msg, success="Success" in msg)

    def _do_renew(self):
        barcode = self.lineEdit_search_input.text().strip()
        if not barcode:
            self._show_msg("Please enter a barcode.", success=False)
            return
        msg = self._capture(MemberService.renew_book, self.librarian, barcode)
        self._show_msg(msg, success="Success" in msg)

    def _do_reserve(self):
        isbn = self.lineEdit_search_input.text().strip()
        if not isbn:
            self._show_msg("Please enter an ISBN.", success=False)
            return
        msg = self._capture(MemberService.reserve_book, self.librarian, isbn)
        self._show_msg(msg, success="Success" in msg)

    def _do_cancel_reservation(self):
        isbn = self.lineEdit_search_input.text().strip()
        if not isbn:
            self._show_msg("Please enter an ISBN.", success=False)
            return
        msg = self._capture(MemberService.cancel_reservation, self.librarian, isbn)
        self._show_msg(msg, success="Success" in msg)

    def _load_my_books(self):
        books = MemberService.get_borrowed_books_list(self.librarian.id)
        self.tableWidget_results.setRowCount(0)
        if not books:
            self._show_msg("You have no books currently checked out.", success=False)
            return
        for row_idx, book in enumerate(books):
            self.tableWidget_results.insertRow(row_idx)
            for col_idx, val in enumerate(book):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget_results.setItem(row_idx, col_idx, item)

    def _load_all_loans(self):
        loans = LibrarianService.get_all_loans_list()
        self.tableWidget_results.setRowCount(0)
        if not loans:
            self._show_msg("No books currently checked out.", success=False)
            return
        for row_idx, loan in enumerate(loans):
            self.tableWidget_results.insertRow(row_idx)
            for col_idx, val in enumerate(loan):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget_results.setItem(row_idx, col_idx, item)

    def _sign_out(self):
        self.login_window.lineEdit_id.clear()
        self.login_window.lineEdit_password.clear()
        self.login_window.label_error.setText("")
        self.login_window.show()
        self.close()
