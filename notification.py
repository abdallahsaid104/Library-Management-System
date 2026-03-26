class Notification:
    def send(self, member, message):
        raise NotImplementedError("Subclass must implement this method")


class EmailNotification(Notification):
    def send(self, member, message):
        print(f"\n[EMAIL SENDING] To: {member.email}")
        print(f"  Subject: Library Notification")
        print(f"  Body: {message}")
        print("[EMAIL SENT SUCCESSFULLY]")


class SMSNotification(Notification):
    def send(self, member, message):
        print(f"\n[SMS SENDING] To: {member.id} ({member.name})")
        print(f"  Msg: {message}")
        print("[SMS SENT SUCCESSFULLY]")
