import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import mysql.connector


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
        self.setWindowTitle('Вход')
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton('Вход', self)
        login_button.clicked.connect(self.accept)

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

    def view_document(self):
        current_item = self.transactions_list.currentItem()

        if current_item is not None:
            index = self.transactions_list.currentRow()
            document_scan = self.transactions[index].document_scan

            if document_scan:
                document_dialog = QDialog(self)
                document_dialog.setWindowTitle('Скан документа')
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
                QMessageBox.warning(self, 'Ошибка',
                                    'Не выбран скан документа для этой транзакции.')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста выберите транзакцию из списка')

    def init_ui(self):
        self.setWindowTitle('Интерфейс админа')

        layout = QVBoxLayout()

        view_document_button = QPushButton('Посмотреть скан документа')
        view_document_button.clicked.connect(self.view_document)
        layout.addWidget(view_document_button)

        # Добавить транзакцию
        add_transaction_layout = QFormLayout()
        self.buyer_input = QLineEdit()
        self.seller_input = QLineEdit()
        self.car_info_input = QLineEdit()
        self.sale_info_input = QLineEdit()
        self.document_scan_input = QLineEdit()
        self.browse_button = QPushButton('Выбрать')
        self.browse_button.clicked.connect(self.browse_document)
        add_transaction_button = QPushButton('Добавить транзакцию')
        add_transaction_button.clicked.connect(self.add_transaction)

        add_transaction_layout.addRow('Покупатель:', self.buyer_input)
        add_transaction_layout.addRow('Продавец:', self.seller_input)
        add_transaction_layout.addRow('Гос.номер/vin:', self.car_info_input)
        add_transaction_layout.addRow('Дата продажи:', self.sale_info_input)
        add_transaction_layout.addRow('Скан документа купли-продажи:', self.document_scan_input)
        add_transaction_layout.addWidget(self.browse_button)
        add_transaction_layout.addWidget(add_transaction_button)

        # Просмотреть транзакции
        view_transactions_layout = QVBoxLayout()
        self.transactions_list = QListWidget()
        view_transactions_layout.addWidget(QLabel('История транзакций:'))
        view_transactions_layout.addWidget(self.transactions_list)

        layout.addLayout(add_transaction_layout)
        layout.addLayout(view_transactions_layout)

        self.setLayout(layout)

        self.update_transactions_list()

    def update_transactions_list(self):
        self.transactions_list.clear()
        for transaction in self.transactions:
            self.transactions_list.addItem(f'Покупатель: {transaction.buyer}, Продавец: {transaction.seller}')

    def browse_document(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Выбрать документ', '',
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

        QMessageBox.information(self, 'Транзакция добавлена', 'Транзакция успешно добавлена')

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

    def add_transaction_to_database(self, transaction):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='mazhorov',
                user='root',
                password='root'
            )

            cursor = connection.cursor()

            # Добавление транзакции в таблицу transactions
            insert_query = """
            INSERT INTO transactions (buyer, seller, car_info, date, document_scan)
            VALUES (%s, %s, %s, %s, %s)
            """
            transaction_data = (
                transaction.buyer,
                transaction.seller,
                transaction.car_info,
                transaction.date,
                transaction.document_scan
            )
            cursor.execute(insert_query, transaction_data)

            connection.commit()
            cursor.close()
            connection.close()

            QMessageBox.information(self, 'Transaction Added', 'Transaction has been added successfully.')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            QMessageBox.warning(self, 'Error', f'Error adding transaction to the database: {err}')

    def delete_transaction_from_database(self, transaction_id):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='mazhorov',
                user='root',
                password='root'
            )

            cursor = connection.cursor()

            # Удаление транзакции из таблицы transactions
            delete_query = "DELETE FROM transactions WHERE id = %s"
            cursor.execute(delete_query, (transaction_id,))

            connection.commit()
            cursor.close()
            connection.close()

            QMessageBox.information(self, 'Transaction Deleted', 'Transaction has been deleted successfully.')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            QMessageBox.warning(self, 'Error', f'Error deleting transaction from the database: {err}')

    def update_transaction_in_database(self, transaction_id, new_data):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='mazhorov',
                user='root',
                password='root'
            )

            cursor = connection.cursor()

            # Изменение данных транзакции в таблице transactions
            update_query = """
            UPDATE transactions
            SET buyer = %s, seller = %s, car_info = %s, date = %s, document_scan = %s
            WHERE id = %s
            """
            updated_data = (
                new_data.buyer,
                new_data.seller,
                new_data.car_info,
                new_data.date,
                new_data.document_scan,
                transaction_id
            )
            cursor.execute(update_query, updated_data)

            connection.commit()
            cursor.close()
            connection.close()

            QMessageBox.information(self, 'Transaction Updated', 'Transaction has been updated successfully.')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            QMessageBox.warning(self, 'Error', f'Error updating transaction in the database: {err}')

    def update_transactions_list(self):
        self.transactions_list.clear()
        for transaction in self.transactions:
            self.transactions_list.addItem(f'Покупатель: {transaction.buyer}, Продавец: {transaction.seller}')

    def init_ui(self):
        self.setWindowTitle('Учет покупок автомобилей')
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

            QMessageBox.warning(self, 'Ошибка', 'Неправильное имя пользователя или пароль')

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
