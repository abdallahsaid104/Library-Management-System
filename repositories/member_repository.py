from person import Member


class MemberRepository:
    def __init__(self, db):
        self.db = db

    def get_member(self, member_id):
        result = self.db.fetch_query("SELECT * FROM members WHERE member_id = ?", (member_id,))
        return Member.from_db_row(result[0]) if result else None

    def update_checkout_count(self, member_id, increment):
        if increment:
            query = "UPDATE members SET checkout_count = checkout_count + 1 WHERE member_id = ?"
        else:
            query = "UPDATE members SET checkout_count = checkout_count - 1 WHERE member_id = ?"
        self.db.execute_query(query, (member_id,))

    def add_reservation(self, member_id, isbn, date):
        self.db.execute_query("INSERT INTO reservations (member_id, isbn, reservation_date) VALUES (?, ?, ?)",
                              (member_id, isbn, str(date)))

    def get_waiting_reservation(self, isbn):
        return self.db.fetch_query("SELECT member_id FROM reservations WHERE isbn = ? AND status = 'waiting' LIMIT 1",
                                   (isbn,))

    def get_reservation(self, member_id, isbn):
        return self.db.fetch_query("SELECT * FROM reservations WHERE member_id = ? AND isbn = ? AND status = 'waiting'",
                                   (member_id, isbn))

    def update_reservation_status(self, member_id, isbn, status):
        self.db.execute_query("UPDATE reservations SET status = ? WHERE member_id = ? AND isbn = ?",
                              (status, member_id, isbn))

    def cancel_reservation(self, member_id, isbn):
        self.db.execute_query("DELETE FROM reservations WHERE member_id = ? AND isbn = ? AND status = 'waiting'",
                              (member_id, isbn))

    def add_member(self, name, member_id, email, password="1234"):
        self.db.execute_query(
            "INSERT INTO members (name, member_id, email, checkout_count, password) VALUES (?, ?, ?, 0, ?)",
            (name, member_id, email, password)
        )

    def delete_member(self, member_id):
        self.db.execute_query("DELETE FROM members WHERE member_id = ?", (member_id,))
