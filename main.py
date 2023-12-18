import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QCloseEvent
from PyQt6.QtCore import Qt
import mysql.connector
from classes import *
from admins import *


class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.password_input = None
        self.username_input = None
        self.main_window = None
        self.users = [
            User("admin", "1", "admin"),
            User("gibdd", "1", "gibdd"),
            User("user", "1", "user")
        ]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Вход')
        self.setGeometry(300, 300, 300, 150)
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton('Вход', self)
        login_button.clicked.connect(self.enter)

        layout.addWidget(QLabel('Имя пользователя:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Пароль:'))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        self.center()
        self.setLayout(layout)

    def center(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def enter(self):
        username = self.username_input.text()
        password = self.password_input.text()

        for user in self.users:
            if user.username == username and user.password == password:
                if user.role == 'admin':
                    self.main_window = AdminInterface()
                    self.main_window.show()
                elif user.role == 'gibdd':
                    self.main_window = GibddInterface()
                    self.main_window.show()
                elif user.role == 'user':
                    self.main_window = UserInterface()
                    self.main_window.show()

                return

        QMessageBox.warning(self, 'Ошибка', 'Неправильное имя пользователя или пароль')

    def show_admin_interface(self):
        self.main_window = AdminInterface()
        self.main_window.show()

    def show_user_interface(self):
        self.main_window = UserInterface()
        self.main_window.show()


def main():
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
