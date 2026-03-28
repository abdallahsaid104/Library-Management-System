import os
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from services.auth_service import AuthService
from styles import (MAIN_STYLE, BUTTON_PRIMARY, BUTTON_ROLE_ACTIVE,
                    BUTTON_ROLE_INACTIVE, LABEL_TITLE, LABEL_SUBTITLE,
                    LABEL_ERROR, LABEL_LINK)

UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "login.ui")


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)

        self._apply_styles()
        self._set_role("member")

        self.button_member.clicked.connect(lambda: self._set_role("member"))
        self.button_librarian.clicked.connect(lambda: self._set_role("librarian"))
        self.button_sign_in.clicked.connect(self._handle_login)
        self.button_create_account.clicked.connect(self._open_register)

        self.member_window = None
        self.librarian_window = None
        self.register_window = None

    def _apply_styles(self):
        self.setStyleSheet(MAIN_STYLE)
        self.label_title.setStyleSheet(LABEL_TITLE)
        self.label_subtitle.setStyleSheet(LABEL_SUBTITLE)
        self.label_error.setStyleSheet(LABEL_ERROR)
        self.button_create_account.setStyleSheet(LABEL_LINK + "background:transparent;border:none;")
        self.button_sign_in.setStyleSheet(BUTTON_PRIMARY)

    def _set_role(self, role):
        self.selected_role = role
        if role == "member":
            self.button_member.setStyleSheet(BUTTON_ROLE_ACTIVE)
            self.button_librarian.setStyleSheet(BUTTON_ROLE_INACTIVE)
            self.button_create_account.setVisible(True)
            self.label_new_member.setVisible(True)
        else:
            self.button_member.setStyleSheet(BUTTON_ROLE_INACTIVE)
            self.button_librarian.setStyleSheet(BUTTON_ROLE_ACTIVE)
            self.button_create_account.setVisible(False)
            self.label_new_member.setVisible(False)
        self.label_error.setText("")

    def _handle_login(self):
        user_id = self.lineEdit_id.text().strip()
        password = self.lineEdit_password.text().strip()

        if not user_id or not password:
            self.label_error.setText("Please fill in all fields.")
            return

        if self.selected_role == "member":
            user = AuthService.login_member(user_id, password)
            if user:
                self._open_member_portal(user)
            else:
                self.label_error.setText("Invalid member ID or password.")
        else:
            user = AuthService.login_librarian(user_id, password)
            if user:
                self._open_librarian_portal(user)
            else:
                self.label_error.setText("Invalid librarian ID or password.")

    def _open_member_portal(self, member):
        from member_window import MemberWindow
        self.member_window = MemberWindow(member, self)
        self.member_window.show()
        self.hide()

    def _open_librarian_portal(self, librarian):
        from librarian_window import LibrarianWindow
        self.librarian_window = LibrarianWindow(librarian, self)
        self.librarian_window.show()
        self.hide()

    def _open_register(self):
        from register_window import RegisterWindow
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()
