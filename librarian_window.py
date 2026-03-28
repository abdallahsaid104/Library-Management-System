import os
import io
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from services.librarian_service import LibrarianService
from services.notification_service import NotificationService
from repositories.loan_repository import LoanRepository
from styles import (MAIN_STYLE, BUTTON_PRIMARY, LABEL_TITLE, LABEL_ERROR,
                    LABEL_SUCCESS, LABEL_SECTION, LABEL_AVATAR,
                    LABEL_MEMBER_NAME, LABEL_BADGE_LIBRARIAN, WIDGET_SIDEBAR,
                    BUTTON_SIGN_OUT)

UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "librarian_portal.ui")


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
            self.button_register_librarian, self.button_overdue
        ]
        self.button_add_book.clicked.connect(self._show_add_book)
        self.button_add_copy.clicked.connect(self._show_add_copy)
        self.button_register_member.clicked.connect(self._show_register_member)
        self.button_cancel_membership.clicked.connect(self._show_cancel_membership)
        self.button_all_loans.clicked.connect(self._show_all_loans)
        self.button_find_borrower.clicked.connect(self._show_find_borrower)
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
        if self.current_page == "add_book":
            msg = self._capture(LibrarianService.add_new_book,
                self.lineEdit_isbn.text().strip(), self.lineEdit_title.text().strip(),
                self.lineEdit_author.text().strip(), self.lineEdit_subject.text().strip(),
                self.lineEdit_pub_date.text().strip())
            self._show_msg(msg, success="Success" in msg)

        elif self.current_page == "add_copy":
            msg = self._capture(LibrarianService.add_book_item,
                self.lineEdit_title.text().strip(),
                self.lineEdit_isbn.text().strip(),
                self.lineEdit_author.text().strip())
            self._show_msg(msg, success="Success" in msg)

        elif self.current_page == "register_member":
            password = self.lineEdit_subject.text().strip() or "1234"
            msg = self._capture(LibrarianService.register_member,
                self.lineEdit_title.text().strip(),
                self.lineEdit_isbn.text().strip(),
                self.lineEdit_author.text().strip(), password)
            self._show_msg(msg, success="Success" in msg)

        elif self.current_page == "cancel_membership":
            msg = self._capture(LibrarianService.cancel_membership,
                self.lineEdit_isbn.text().strip())
            self._show_msg(msg, success="Success" in msg)

        elif self.current_page == "find_borrower":
            msg = self._capture(LibrarianService.get_book_borrower,
                self.lineEdit_isbn.text().strip())
            self._show_msg(msg, success="currently borrowed" in msg)

        elif self.current_page == "register_librarian":
            msg = self._capture(LibrarianService.register_librarian,
                self.lineEdit_title.text().strip(),
                self.lineEdit_isbn.text().strip(),
                self.lineEdit_author.text().strip(),
                self.lineEdit_subject.text().strip())
            self._show_msg(msg, success="Success" in msg)

        elif self.current_page == "overdue":
            msg = self._capture(NotificationService.check_overdue)
            self._show_msg(msg, success="No overdue" in msg)

    def _handle_secondary(self):
        if self.current_page == "add_book":
            msg = self._capture(LibrarianService.edit_book,
                self.lineEdit_isbn.text().strip(),
                self.lineEdit_title.text().strip() or None,
                self.lineEdit_author.text().strip() or None,
                self.lineEdit_subject.text().strip() or None)
            self._show_msg(msg, success="Success" in msg)

        elif self.current_page == "add_copy":
            msg = self._capture(LibrarianService.remove_book_item,
                self.lineEdit_title.text().strip())
            self._show_msg(msg, success="Success" in msg)

    def _load_all_loans(self):
        loans = LoanRepository.get_all_active_loans()
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
