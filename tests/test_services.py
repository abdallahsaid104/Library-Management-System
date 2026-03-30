import pytest
from unittest.mock import MagicMock, patch, call
from datetime import date
from services.auth_service import AuthService


# ------------------------------- Helpers ---------------------------------------
def make_member(name="zezo", member_id="MEM-001", email="ahmed@email.com", checkout_count=0):
    m = MagicMock()
    m.name = name
    m.id = member_id
    m.email = email
    m.checkout_count = checkout_count
    m.MaxBooksLimit = 5
    m.can_checkout.return_value = checkout_count < 5
    m.get_due_date.return_value = date(2026, 4, 10)
    m.calculate_fine.return_value = 0
    m.check_password.return_value = True
    return m


def make_librarian(name="Admin", librarian_id="LIB-001", email="admin@lib.com"):
    lib = MagicMock()
    lib.name = name
    lib.id = librarian_id
    lib.email = email
    lib.check_password.return_value = True
    return lib


class TestAuthService:

    @patch("services.auth_service.DatabaseManager")
    @patch("services.auth_service.MemberRepository")
    def test_login_member_success(self, member_repository, db):
        member = make_member()
        member_repo = MagicMock()
        member_repo.get_member.return_value = member
        member_repository.return_value = member_repo
        db.return_value.__enter__ = MagicMock(return_value=MagicMock())
        db.return_value.__exit__ = MagicMock(return_value=False)

        result = AuthService.login_member("MEM-001", "1234")
        assert result == member

    @patch("services.auth_service.DatabaseManager")
    @patch("services.auth_service.MemberRepository")
    def test_login_member_not_found(self, member_repository, db):
        mock_repo = MagicMock()
        mock_repo.get_member.return_value = None
        member_repository.return_value = mock_repo
        db.return_value.__enter__ = MagicMock(return_value=MagicMock())
        db.return_value.__exit__ = MagicMock(return_value=False)

        result = AuthService.login_member("MEM-999", "5678")
        assert result is None

    @patch("services.auth_service.DatabaseManager")
    @patch("services.auth_service.MemberRepository")
    def test_login_member_wrong_password(self, member_repository, db):
        member = make_member()
        member.check_password.return_value = False
        mock_repo = MagicMock()
        mock_repo.get_member.return_value = member
        member_repository.return_value = mock_repo
        db.return_value.__enter__ = MagicMock(return_value=MagicMock())
        db.return_value.__exit__ = MagicMock(return_value=False)

        result = AuthService.login_member("MEM-001", "admin")
        assert result is None

    @patch("services.auth_service.DatabaseManager")
    @patch("services.auth_service.LibrarianRepository")
    def test_login_librarian_success(self, librarian_repository, db):
        librarian = make_librarian()
        mock_repo = MagicMock()
        mock_repo.get_librarian.return_value = librarian
        librarian_repository.return_value = mock_repo
        db.return_value.__enter__ = MagicMock(return_value=MagicMock())
        db.return_value.__exit__ = MagicMock(return_value=False)

        result = AuthService.login_librarian("LIB-001", "correct_password")
        assert result == librarian

    @patch("services.auth_service.DatabaseManager")
    @patch("services.auth_service.LibrarianRepository")
    def test_login_librarian_not_found(self, librarian_repository, db):
        mock_repo = MagicMock()
        mock_repo.get_librarian.return_value = None
        librarian_repository.return_value = mock_repo
        db.return_value.__enter__ = MagicMock(return_value=MagicMock())
        db.return_value.__exit__ = MagicMock(return_value=False)

        result = AuthService.login_librarian("LIB-999", "any")
        assert result is None

    @patch("services.auth_service.DatabaseManager")
    @patch("services.auth_service.LibrarianRepository")
    def test_login_librarian_wrong_password(self, librarian_repository, db):
        librarian = make_librarian()
        librarian.check_password.return_value = False
        mock_repo = MagicMock()
        mock_repo.get_librarian.return_value = librarian
        librarian_repository.return_value = mock_repo
        db.return_value.__enter__ = MagicMock(return_value=MagicMock())
        db.return_value.__exit__ = MagicMock(return_value=False)

        result = AuthService.login_librarian("LIB-001", "wrong_password")
        assert result is None
