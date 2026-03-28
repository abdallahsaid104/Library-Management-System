from person import Member, Librarian


class AuthService:

    @staticmethod
    def login_member(member_id, password):
        member = Member.get_member(member_id)
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
        librarian = Librarian.get_librarian(librarian_id)
        if not librarian:
            print("ERROR: Librarian not found.")
            return None
        if not librarian.check_password(password):
            print("ERROR: Incorrect password")
            return None
        print(f"Welcome {librarian.name}")
        return librarian
