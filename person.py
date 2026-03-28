from database import DatabaseManager
from datetime import datetime, timedelta
from abc import ABC


class Person(ABC):
    def __init__(self, name, person_id, email):
        self.name = name
        self.id = person_id
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

    def __init__(self, name, person_id, email, checkout_count=0):
        super().__init__(name, person_id, email)
        self.checkout_count = checkout_count

    def can_checkout(self):
        return self.checkout_count < self.MaxBooksLimit

    def get_due_date(self):
        return datetime.now().date() + timedelta(self.MaxDaysLimit)

    def calculate_fine(self, today, due_date):
        fine = 0
        if today > due_date:
            days_late = (today-due_date).days
            fine = days_late * self.FinePerDay
            print(f"Book is {days_late} days late : Fine ----> {fine} Egyptian bound")
        else:
            print(f"Book is returned on time, No Fine")

        return fine

    @staticmethod
    def get_member(member_id):
        db = DatabaseManager()
        query = "SELECT * FROM members WHERE member_id = ?"
        member = db.fetch_query(query, (member_id,))
        db.close()
        if member:
            return Member(member[0][0], member[0][1], member[0][2], member[0][3])
        return None


class Librarian(Person):
    def __init__(self, name, employee_id, email):
        super().__init__(name, employee_id, email)
