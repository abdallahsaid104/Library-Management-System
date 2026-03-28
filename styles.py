MAIN_STYLE = """
QDialog, QMainWindow, QWidget {
    background-color: #1a1f2e;
    color: #ffffff;
    font-family: Segoe UI;
    font-size: 13px;
}

QLabel {
    color: #cccccc;
    font-size: 13px;
}

QLineEdit {
    background-color: #2a2f3e;
    color: #ffffff;
    border: 1px solid #3a3f4e;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    min-height: 36px;
}

QLineEdit:focus {
    border: 1px solid #4a90d9;
}

QLineEdit::placeholder {
    color: #666c7a;
}

QComboBox {
    background-color: #2a2f3e;
    color: #ffffff;
    border: 1px solid #3a3f4e;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    min-height: 36px;
}

QComboBox:focus {
    border: 1px solid #4a90d9;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #2a2f3e;
    color: #ffffff;
    border: 1px solid #3a3f4e;
    selection-background-color: #4a90d9;
}

QPushButton {
    background-color: #2a2f3e;
    color: #ffffff;
    border: 1px solid #3a3f4e;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
    min-height: 36px;
}

QPushButton:hover {
    background-color: #353b4e;
    border: 1px solid #4a90d9;
}

QPushButton:pressed {
    background-color: #2a2f3e;
}

QPushButton[flat=true] {
    background-color: transparent;
    border: none;
    color: #4a90d9;
    text-align: left;
    padding: 6px 10px;
    min-height: 30px;
}

QPushButton[flat=true]:hover {
    background-color: #2a2f3e;
    border-radius: 6px;
    color: #ffffff;
}

QPushButton[flat=true]:checked {
    background-color: #2a2f3e;
    color: #ffffff;
    font-weight: bold;
    border-radius: 6px;
}

QTableWidget {
    background-color: #22273a;
    color: #ffffff;
    border: 1px solid #3a3f4e;
    border-radius: 6px;
    gridline-color: #2a2f3e;
    font-size: 13px;
}

QTableWidget::item {
    padding: 6px 10px;
}

QTableWidget::item:selected {
    background-color: #4a90d9;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #1a1f2e;
    color: #888888;
    border: none;
    border-bottom: 1px solid #3a3f4e;
    padding: 6px 10px;
    font-size: 12px;
}

QFrame[frameShape="4"] {
    color: #3a3f4e;
}

QScrollBar:vertical {
    background: #1a1f2e;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #3a3f4e;
    border-radius: 4px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

BUTTON_PRIMARY = """
    background-color: #4a90d9;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    min-height: 40px;
"""

BUTTON_PRIMARY_HOVER = """
    background-color: #4a90d9;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    min-height: 40px;
"""

BUTTON_ROLE_ACTIVE = """
    background-color: #4a90d9;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    min-height: 36px;
    padding: 6px 16px;
"""

BUTTON_ROLE_INACTIVE = """
    background-color: #2a2f3e;
    color: #aaaaaa;
    border: 1px solid #3a3f4e;
    border-radius: 6px;
    font-size: 13px;
    min-height: 36px;
    padding: 6px 16px;
"""

LABEL_TITLE = """
    color: #ffffff;
    font-size: 28px;
    font-weight: bold;
"""

LABEL_SUBTITLE = """
    color: #888888;
    font-size: 13px;
"""

LABEL_FIELD = """
    color: #cccccc;
    font-size: 12px;
    margin-bottom: 2px;
"""

LABEL_ERROR = """
    color: #e05555;
    font-size: 12px;
"""

LABEL_SUCCESS = """
    color: #4caf50;
    font-size: 12px;
"""

LABEL_LINK = """
    color: #4a90d9;
    font-size: 13px;
"""

LABEL_SECTION = """
    color: #555c6e;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1px;
    margin-top: 8px;
"""

LABEL_AVATAR = """
    background-color: #2a3f5e;
    color: #4a90d9;
    border-radius: 20px;
    font-size: 14px;
    font-weight: bold;
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
"""

LABEL_MEMBER_NAME = """
    color: #ffffff;
    font-size: 13px;
    font-weight: bold;
"""

LABEL_BADGE_MEMBER = """
    color: #4a90d9;
    background-color: #1a2f4e;
    border-radius: 8px;
    font-size: 11px;
    padding: 2px 8px;
"""

LABEL_BADGE_LIBRARIAN = """
    color: #4caf50;
    background-color: #1a3a2e;
    border-radius: 8px;
    font-size: 11px;
    padding: 2px 8px;
"""

WIDGET_SIDEBAR = """
    background-color: #141824;
    border-right: 1px solid #2a2f3e;
"""

BUTTON_SIGN_OUT = """
    background-color: transparent;
    border: none;
    color: #e05555;
    text-align: left;
    padding: 6px 10px;
    min-height: 30px;
    font-size: 13px;
"""
