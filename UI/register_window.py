import os
import io
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from services.librarian_service import LibrarianService
from UI.styles import (MAIN_STYLE, BUTTON_PRIMARY, LABEL_TITLE,
                       LABEL_SUBTITLE, LABEL_ERROR, LABEL_SUCCESS, LABEL_LINK)

UI_PATH = os.path.join(os.path.dirname(__file__), "", "register.ui")

"""
The application stores all its data in a single SQLite database file called library.db, which contains six tables. When the application starts, it automatically checks if these tables exist and creates them if they don’t. This setup is handled by the DatabaseManager. The process is safe to run every time the app starts, because it won’t recreate or overwrite tables that already exist.
"""
class RegisterWindow(QDialog):
    def __init__(self, login_window):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.login_window = login_window

        self._apply_styles()

        self.button_register.clicked.connect(self._handle_register)
        self.button_back.clicked.connect(self._go_back)

    def _apply_styles(self):
        self.setStyleSheet(MAIN_STYLE)
        self.label_title.setStyleSheet(LABEL_TITLE)
        self.label_subtitle.setStyleSheet(LABEL_SUBTITLE)
        self.label_error.setStyleSheet(LABEL_ERROR)
        self.button_register.setStyleSheet(BUTTON_PRIMARY)
        self.button_back.setStyleSheet(
            LABEL_LINK + "background:transparent;border:none;text-align:center;"
        )

    def _capture(self, func, *args, **kwargs):
        captured = io.StringIO()
        sys.stdout = captured
        func(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return captured.getvalue().strip()

    def _handle_register(self):
        name = self.lineEdit_full_name.text().strip()
        member_id = self.lineEdit_member_id.text().strip()
        email = self.lineEdit_email.text().strip()
        password = self.lineEdit_password.text().strip()

        if not all([name, member_id, email, password]):
            self.label_error.setStyleSheet(LABEL_ERROR)
            self.label_error.setText("Please fill in all fields.")
            return

        msg = self._capture(LibrarianService.register_member, name, member_id, email, password)

        if "Success" in msg:
            self.label_error.setStyleSheet(LABEL_SUCCESS)
            self.label_error.setText(msg)
            self.lineEdit_full_name.clear()
            self.lineEdit_member_id.clear()
            self.lineEdit_email.clear()
            self.lineEdit_password.clear()
        else:
            self.label_error.setStyleSheet(LABEL_ERROR)
            self.label_error.setText(msg)

    def _go_back(self):
        self.login_window.show()
        self.close()
