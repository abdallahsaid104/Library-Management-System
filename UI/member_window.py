import os
import io
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from services.member_service import MemberService
from UI.styles import (MAIN_STYLE, BUTTON_PRIMARY, LABEL_TITLE, LABEL_ERROR,
                       LABEL_SUCCESS, LABEL_SECTION, LABEL_AVATAR,
                       LABEL_MEMBER_NAME, LABEL_BADGE_MEMBER, WIDGET_SIDEBAR,
                       BUTTON_SIGN_OUT)

UI_PATH = os.path.join(os.path.dirname(__file__), "", "member_portal.ui")


class MemberWindow(QMainWindow):
    def __init__(self, member, login_window):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.member = member
        self.login_window = login_window

        self._apply_styles()
        self._setup_profile()
        self._connect_nav()
        self.current_page = "search"
        self._show_search()

    def _apply_styles(self):
        self.setStyleSheet(MAIN_STYLE)
        self.widget_sidebar.setStyleSheet(WIDGET_SIDEBAR)
        self.label_page_title.setStyleSheet(LABEL_TITLE)
        self.label_avatar.setStyleSheet(LABEL_AVATAR)
        self.label_member_name.setStyleSheet(LABEL_MEMBER_NAME)
        self.label_member_badge.setStyleSheet(LABEL_BADGE_MEMBER)
        self.label_section_books.setStyleSheet(LABEL_SECTION)
        self.label_section_reservations.setStyleSheet(LABEL_SECTION)
        self.label_section_account.setStyleSheet(LABEL_SECTION)
        self.label_result_msg.setStyleSheet(LABEL_ERROR)
        self.button_action.setStyleSheet(BUTTON_PRIMARY)
        self.button_sign_out.setStyleSheet(BUTTON_SIGN_OUT)

    def _setup_profile(self):
        initials = "".join(w[0].upper() for w in self.member.name.split()[:2])
        self.label_avatar.setText(initials)
        self.label_member_name.setText(self.member.name)

    def _connect_nav(self):
        self.nav_buttons = [
            self.button_search, self.button_checkout, self.button_return,
            self.button_renew, self.button_reserve,
            self.button_cancel_reservation, self.button_my_books
        ]
        self.button_search.clicked.connect(self._show_search)
        self.button_checkout.clicked.connect(self._show_checkout)
        self.button_return.clicked.connect(self._show_return)
        self.button_renew.clicked.connect(self._show_renew)
        self.button_reserve.clicked.connect(self._show_reserve)
        self.button_cancel_reservation.clicked.connect(self._show_cancel_reservation)
        self.button_my_books.clicked.connect(self._show_my_books)
        self.button_sign_out.clicked.connect(self._sign_out)
        self.button_action.clicked.connect(self._handle_action)

    def _set_active_nav(self, active):
        for btn in self.nav_buttons:
            btn.setChecked(btn == active)

    def _clear_content(self):
        self.comboBox_search_type.setVisible(False)
        self.lineEdit_search_input.setVisible(False)
        self.lineEdit_search_input.clear()
        self.tableWidget_results.setVisible(False)
        self.label_result_msg.setText("")
        self.button_action.setVisible(True)

    def _show_search(self):
        self._clear_content()
        self._set_active_nav(self.button_search)
        self.current_page = "search"
        self.label_page_title.setText("Search catalog")
        self.comboBox_search_type.setVisible(True)
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter search term...")
        self.button_action.setText("Search")
        self.tableWidget_results.setVisible(True)
        self._setup_table(["Title", "Author", "Subject", "ISBN"])

    def _show_checkout(self):
        self._clear_content()
        self._set_active_nav(self.button_checkout)
        self.current_page = "checkout"
        self.label_page_title.setText("Check out book")
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter book barcode...")
        self.button_action.setText("Check out")

    def _show_return(self):
        self._clear_content()
        self._set_active_nav(self.button_return)
        self.current_page = "return"
        self.label_page_title.setText("Return book")
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter book barcode...")
        self.button_action.setText("Return book")

    def _show_renew(self):
        self._clear_content()
        self._set_active_nav(self.button_renew)
        self.current_page = "renew"
        self.label_page_title.setText("Renew book")
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter book barcode...")
        self.button_action.setText("Renew")

    def _show_reserve(self):
        self._clear_content()
        self._set_active_nav(self.button_reserve)
        self.current_page = "reserve"
        self.label_page_title.setText("Reserve book")
        self.lineEdit_search_input.setVisible(True)
        self.lineEdit_search_input.setPlaceholderText("Enter book ISBN...")
        self.button_action.setText("Reserve")

    def _show_cancel_reservation(self):
        self._clear_content()
        self._set_active_nav(self.button_cancel_reservation)
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

    def _handle_action(self):
        page_map = {
            "search": self._do_search,
            "checkout": self._do_checkout,
            "return": self._do_return,
            "renew": self._do_renew,
            "reserve": self._do_reserve,
            "cancel_res": self._do_cancel_reservation,
        }
        if self.current_page in page_map:
            page_map[self.current_page]()

    def _capture(self, func, *args, **kwargs):
        captured = io.StringIO()
        sys.stdout = captured
        func(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return captured.getvalue().strip()

    def _show_msg(self, msg, success=True):
        self.label_result_msg.setStyleSheet(LABEL_SUCCESS if success else LABEL_ERROR)
        self.label_result_msg.setText(msg)

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
        msg = self._capture(MemberService.checkout_book, self.member, barcode)
        self._show_msg(msg, success="Success" in msg)

    def _do_return(self):
        barcode = self.lineEdit_search_input.text().strip()
        if not barcode:
            self._show_msg("Please enter a barcode.", success=False)
            return
        msg = self._capture(MemberService.return_book, self.member, barcode)
        self._show_msg(msg, success="Success" in msg)

    def _do_renew(self):
        barcode = self.lineEdit_search_input.text().strip()
        if not barcode:
            self._show_msg("Please enter a barcode.", success=False)
            return
        msg = self._capture(MemberService.renew_book, self.member, barcode)
        self._show_msg(msg, success="Success" in msg)

    def _do_reserve(self):
        isbn = self.lineEdit_search_input.text().strip()
        if not isbn:
            self._show_msg("Please enter an ISBN.", success=False)
            return
        msg = self._capture(MemberService.reserve_book, self.member, isbn)
        self._show_msg(msg, success="Success" in msg)

    def _do_cancel_reservation(self):
        isbn = self.lineEdit_search_input.text().strip()
        if not isbn:
            self._show_msg("Please enter an ISBN.", success=False)
            return
        msg = self._capture(MemberService.cancel_reservation, self.member, isbn)
        self._show_msg(msg, success="Success" in msg)

    def _load_my_books(self):
        books = MemberService.get_borrowed_books_list(self.member.id)

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

    def _sign_out(self):
        self.login_window.lineEdit_id.clear()
        self.login_window.lineEdit_password.clear()
        self.login_window.label_error.setText("")
        self.login_window.show()
        self.close()
