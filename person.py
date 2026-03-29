from datetime import datetime, timedelta


class Person:
    def __init__(self, name, person_id, email):
        self.id = person_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"Name: {self.name}\nID:   {self.id}\nEmail:{self.email}"


class Member(Person):
    MaxBooksLimit = 5
    MaxDaysLimit = 10
    FinePerDay = 5

    def __init__(self, name, member_id, email, checkout_count=0, password=None):
        super().__init__(name, member_id, email)
        self.checkout_count = checkout_count
        self.password = password

    def __str__(self):
        base_info = super().__str__()
        return f"{base_info}\nChecked Out: {self.checkout_count}/{self.MaxBooksLimit}"

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

    @classmethod
    def from_db_row(cls, row):
        return cls(row[0], row[1], row[2], row[3], row[4])


class Librarian(Member):
    def __init__(self, name, librarian_id, email, checkout_count=0, password=None):
        super().__init__(name, librarian_id, email, checkout_count, password)

    def __str__(self):
        base_info = super().__str__()
        return f"{base_info}\nRole: Librarian"

    @classmethod
    def from_db_row(cls, row):
        return cls(row[0], row[1], row[2], row[3], row[4])
