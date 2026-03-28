from datetime import datetime, timedelta
from repositories.member_repository import MemberRepository
from repositories.librarian_repository import LibrarianRepository


class Person:
    def __init__(self, name, person_id, email):
        self.id = person_id
        self.name = name
        self.email = email

    def __str__(self):
        info = f"""
Name: {self.name}
ID:   {self.id}
Email:{self.email}"""
        return info


class Member(Person):
    MaxBooksLimit = 5
    MaxDaysLimit = 10
    FinePerDay = 5

    def __init__(self, name, member_id, email, checkout_count=0, password=None):
        super().__init__(name, member_id, email)
        self.checkout_count = checkout_count
        self.password = password

    def check_password(self, input_password):
        return self.password == input_password

    def can_checkout(self):
        return self.checkout_count < self.MaxBooksLimit

    def get_due_date(self):
        return datetime.now().date() + timedelta(self.MaxDaysLimit)

    def calculate_fine(self, today, due_date):
        fine = 0
        if today > due_date:
            days_late = (today - due_date).days
            fine = days_late * self.FinePerDay
            print(f"Book is {days_late} days late : Fine ----> {fine} Egyptian bound")
        else:
            print(f"Book is returned on time, No Fine")
        return fine

    @staticmethod
    def get_member(member_id):
        member = MemberRepository.get_member(member_id)
        if member:
            return Member(member[0][0], member[0][1], member[0][2], member[0][3], member[0][4])
        return None


class Librarian(Person):
    def __init__(self, name, librarian_id, email, password=None):
        super().__init__(name, librarian_id, email)
        self.password = password

    def check_password(self, input_password):
        return self.password == input_password

    @staticmethod
    def get_librarian(librarian_id):
        librarian = LibrarianRepository.get_librarian(librarian_id)
        if librarian:
            return Librarian(librarian[0][0], librarian[0][1], librarian[0][2], librarian[0][3])
        return None
