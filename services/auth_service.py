from database import DatabaseManager
from person import Member, Librarian
from repositories.member_repository import MemberRepository
from repositories.librarian_repository import LibrarianRepository


class AuthService:

    @staticmethod
    def login_member(member_id, password):
        with DatabaseManager() as db:
            repo = MemberRepository(db)
            member = repo.get_member(member_id)

        if not member:
            print("ERROR: Member not found")
            return None
        if not member.check_password(password):
            print("ERROR: Incorrect password")
            return None
        print(f"Welcome {member.name}")
        return member

    @staticmethod
    def login_librarian(librarian_id, password):
        with DatabaseManager() as db:
            repo = LibrarianRepository(db)
            librarian = repo.get_librarian(librarian_id)

        if not librarian:
            print("ERROR: Librarian not found")
            return None
        if not librarian.check_password(password):
            print("ERROR: Incorrect password")
            return None
        print(f"Welcome {librarian.name}")
        return librarian
