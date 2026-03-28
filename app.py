import sys
from PyQt5.QtWidgets import QApplication
from database import DatabaseManager
from login_window import LoginWindow


def main():
    db = DatabaseManager()
    db.add_dummy_data()
    db.close()

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
