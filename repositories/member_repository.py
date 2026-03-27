from database import DatabaseManager


class MemberRepository:

    @staticmethod
    def get_member(member_id):
        db = DatabaseManager()
        member = db.fetch_query("SELECT * FROM members WHERE member_id = ?", (member_id,))
        db.close()
        return member

    @staticmethod
    def update_checkout_count(member_id, increment):
        db = DatabaseManager()
        if increment:
            query = "UPDATE members SET checkout_count = checkout_count + 1 WHERE member_id = ?"
        else:
            query = "UPDATE members SET checkout_count = checkout_count - 1 WHERE member_id = ?"
        db.execute_query(query, (member_id,))
        db.close()

    @staticmethod
    def add_reservation(member_id, isbn, date):
        db = DatabaseManager()
        db.execute_query("INSERT INTO reservations (member_id, isbn, reservation_date) VALUES (?, ?, ?)",
                         (member_id, isbn, str(date)))
        db.close()

    @staticmethod
    def get_waiting_reservation(isbn):
        db = DatabaseManager()
        query = "SELECT member_id FROM reservations WHERE isbn = ? AND status = 'waiting' LIMIT 1"
        result = db.fetch_query(query, (isbn,))
        db.close()
        return result

    @staticmethod
    def get_reservation(member_id, isbn):
        db = DatabaseManager()
        reservation = db.fetch_query(
            "SELECT * FROM reservations WHERE member_id = ? AND isbn = ? AND status = 'waiting'",
            (member_id, isbn)
        )
        db.close()
        return reservation

    @staticmethod
    def update_reservation_status(member_id, isbn, status):
        db = DatabaseManager()
        db.execute_query("UPDATE reservations SET status = ? WHERE member_id = ? AND isbn = ?",
                         (status, member_id, isbn))
        db.close()

    @staticmethod
    def cancel_reservation(member_id, isbn):
        db = DatabaseManager()
        db.execute_query("DELETE FROM reservations WHERE member_id = ? AND isbn = ? AND status = 'waiting'",
                         (member_id, isbn))
        db.close()

    @staticmethod
    def add_member(name, member_id, email):
        db = DatabaseManager()
        db.execute_query(
            "INSERT INTO members (name, member_id, email, checkout_count) VALUES (?, ?, ?, 0)",
            (name, member_id, email)
        )
        db.close()

    @staticmethod
    def delete_member(member_id):
        db = DatabaseManager()
        db.execute_query("DELETE FROM members WHERE member_id = ?", (member_id,))
        db.close()
