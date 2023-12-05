import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QMessageBox, QListWidget, QDialog, QVBoxLayout, QFormLayout, QFileDialog, QSplashScreen
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.accept)

        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        self.setLayout(layout)


class Transaction:
    def __init__(self, buyer, seller, car_info, sale_info, document_scan):
        self.buyer = buyer
        self.seller = seller
        self.car_info = car_info
        self.sale_info = sale_info
        self.document_scan = document_scan


class AdminInterface(QDialog):
    def __init__(self, transactions):
        super().__init__()

        self.transactions = transactions

        self.init_ui()

    def closeEvent(self, event):
        # Переопределяем метод closeEvent для обработки закрытия окна
        QApplication.quit()

    def view_document(self):
        current_item = self.transactions_list.currentItem()

        if current_item is not None:
            index = self.transactions_list.currentRow()
            document_scan = self.transactions[index].document_scan

            if document_scan:
                document_dialog = QDialog(self)
                document_dialog.setWindowTitle('Document Scan')
                document_dialog.setGeometry(100, 100, 400, 400)

                layout = QVBoxLayout()

                document_label = QLabel()
                pixmap = QPixmap(document_scan)
                document_label.setPixmap(pixmap)
                document_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                layout.addWidget(document_label)
                document_dialog.setLayout(layout)

                document_dialog.exec()

            else:
                QMessageBox.warning(self, 'No Document Scan', 'No document scan available for this transaction.')
        else:
            QMessageBox.warning(self, 'Select Transaction', 'Please select a transaction from the list.')

    def init_ui(self):
        self.setWindowTitle('Admin Interface')

        layout = QVBoxLayout()

        view_document_button = QPushButton('View Document Scan')
        view_document_button.clicked.connect(self.view_document)
        layout.addWidget(view_document_button)

        # Добавить транзакцию
        add_transaction_layout = QFormLayout()
        self.buyer_input = QLineEdit()
        self.seller_input = QLineEdit()
        self.car_info_input = QLineEdit()
        self.sale_info_input = QLineEdit()
        self.document_scan_input = QLineEdit()
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_document)
        add_transaction_button = QPushButton('Add Transaction')
        add_transaction_button.clicked.connect(self.add_transaction)

        add_transaction_layout.addRow('Buyer:', self.buyer_input)
        add_transaction_layout.addRow('Seller:', self.seller_input)
        add_transaction_layout.addRow('Car Info:', self.car_info_input)
        add_transaction_layout.addRow('Sale Info:', self.sale_info_input)
        add_transaction_layout.addRow('Document Scan:', self.document_scan_input)
        add_transaction_layout.addWidget(self.browse_button)
        add_transaction_layout.addWidget(add_transaction_button)

        # Просмотреть транзакции
        view_transactions_layout = QVBoxLayout()
        self.transactions_list = QListWidget()
        view_transactions_layout.addWidget(QLabel('Transaction History:'))
        view_transactions_layout.addWidget(self.transactions_list)

        layout.addLayout(add_transaction_layout)
        layout.addLayout(view_transactions_layout)

        self.setLayout(layout)

        self.update_transactions_list()

    def update_transactions_list(self):
        self.transactions_list.clear()
        for transaction in self.transactions:
            self.transactions_list.addItem(f'Buyer: {transaction.buyer}, Seller: {transaction.seller}')

    def browse_document(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Document Scan', '',
                                                   'Image Files (*.png *.jpg *.bmp *.gif *.jpeg)')

        if file_path:
            self.document_scan_input.setText(file_path)

    def add_transaction(self):
        buyer = self.buyer_input.text()
        seller = self.seller_input.text()
        car_info = self.car_info_input.text()
        sale_info = self.sale_info_input.text()
        document_scan = self.document_scan_input.text()

        new_transaction = Transaction(buyer, seller, car_info, sale_info, document_scan)
        self.transactions.append(new_transaction)

        QMessageBox.information(self, 'Transaction Added', 'Transaction has been added successfully.')

        self.clear_inputs()
        self.update_transactions_list()

    def clear_inputs(self):
        self.buyer_input.clear()
        self.seller_input.clear()
        self.car_info_input.clear()
        self.sale_info_input.clear()
        self.document_scan_input.clear()

    def closeEvent(self, event):
        QApplication.quit()


class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.users = [
            User("admin", "1", "admin"),
            User("gibdd", "1111", "gibdd"),
            User("user", "1111", "user")
        ]

        self.transactions = []

        self.init_ui()

    def update_transactions_list(self):
        self.transactions_list.clear()
        for transaction in self.transactions:
            self.transactions_list.addItem(f'Buyer: {transaction.buyer}, Seller: {transaction.seller}')

    def init_ui(self):
        self.setWindowTitle('Car Transactions System')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.show_login_dialog()

    def show_login_dialog(self):
        login_dialog = LoginDialog()
        result = login_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            username = login_dialog.username_input.text()
            password = login_dialog.password_input.text()

            for user in self.users:
                if user.username == username and user.password == password:
                    if user.role == 'admin':
                        self.show_admin_interface()
                    elif user.role == 'gibdd':
                        self.show_gibdd_interface()
                    elif user.role == 'user':
                        self.show_user_interface()
                    return

            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')

            # Если логин не прошел успешно, повторно вызываем окно логина
            self.show_login_dialog()

        else:
            # Если пользователь закрыл окно, завершаем приложение
            sys.exit()

    def show_admin_interface(self):
        self.admin_interface = AdminInterface(self.transactions)
        result = self.admin_interface.exec()



        self.close()

    def show_gibdd_interface(self):
        # Здесь вы можете добавить интерфейс для сотрудника ГИБДД
        pass

    def show_user_interface(self):
        # Здесь вы можете добавить интерфейс для обычного пользователя
        pass


def main():
    app = QApplication(sys.argv)
    main_app = MainApp()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
