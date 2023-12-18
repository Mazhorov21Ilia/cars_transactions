import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QCloseEvent
from PyQt6.QtCore import Qt
import mysql.connector
from classes import *


class AdminInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.car_cost_input = None
        self.place_of_contract_input = None
        self.date_input = None
        self.car_info_input = None
        self.seller_input = None
        self.buyer_input = None
        self.transactions_list = None
        self.transactions = []
        self.setGeometry(730, 300, 500, 500)
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Transactions"
        )
        self.cursor = self.connection.cursor()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Интерфейс администратора')

        layout = QVBoxLayout()

        view_transactions_layout = QVBoxLayout()
        self.transactions_list = QListWidget()
        view_transactions_layout.addWidget(QLabel('История транзакций:'))
        view_transactions_layout.addWidget(self.transactions_list)

        add_transaction_layout = QFormLayout()
        self.buyer_input = QLineEdit()
        self.buyer_input.setPlaceholderText("фио")
        self.seller_input = QLineEdit()
        self.seller_input.setPlaceholderText("фио")
        self.car_info_input = QLineEdit()
        self.car_info_input.setPlaceholderText("марка")
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("гггг-мм-дд")
        self.place_of_contract_input = QLineEdit()
        self.place_of_contract_input.setPlaceholderText("адрес")
        self.car_cost_input = QLineEdit()
        self.car_cost_input.setPlaceholderText("р.")

        add_transaction_button = QPushButton('Добавить транзакцию')
        add_transaction_button.clicked.connect(self.add_transaction)

        add_transaction_layout.addRow('Покупатель:', self.buyer_input)
        add_transaction_layout.addRow('Продавец:', self.seller_input)
        add_transaction_layout.addRow('Марка авто:', self.car_info_input)
        add_transaction_layout.addRow('Дата транзакции:', self.date_input)
        add_transaction_layout.addRow('Место подписания договора:', self.place_of_contract_input)
        add_transaction_layout.addRow('Стоимость:', self.car_cost_input)
        add_transaction_layout.addWidget(add_transaction_button)

        delete_transaction_layout = QVBoxLayout()
        delete_transaction_button = QPushButton('Удалить транзакцию')
        delete_transaction_button.clicked.connect(self.delete_transaction)
        delete_transaction_layout.addWidget(delete_transaction_button)

        layout.addLayout(delete_transaction_layout)

        layout.addLayout(add_transaction_layout)
        layout.addLayout(view_transactions_layout)
        self.setLayout(layout)

        self.fetch_transactions_from_database()

    def fetch_transactions_from_database(self):
        try:
            self.transactions = []
            select_query = "SELECT buyer, seller, car_info, date, Address, Cost FROM transaction"
            self.cursor.execute(select_query)

            rows = self.cursor.fetchall()

            for row in rows:
                buyer, seller, car_info, date, place_of_contract, car_cost = row
                transaction = Transaction(buyer, seller, car_info, date, place_of_contract, car_cost)
                self.transactions.append(transaction)

            self.update_transactions_list()

        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")
            QMessageBox.warning(self, 'Ошибка', f'Ошибка импорта транзакций из базы данных: {err}')

    def update_transactions_list(self):
        self.transactions_list.clear()
        for transaction in self.transactions:
            self.transactions_list.addItem(f'Покупатель: {transaction.buyer}, '
                                           f'Продавец: {transaction.seller}, '
                                           f'Марка авто: {transaction.car_info}, '
                                           f'Дата транзакции: {transaction.date}, '
                                           f'Место подписания договора: {transaction.place_of_contract}, '
                                           f'Стоимость: {transaction.car_cost}')

    def add_transaction(self):
        try:
            buyer = self.buyer_input.text()
            seller = self.seller_input.text()
            car_info = self.car_info_input.text()
            date = self.date_input.text()
            place_of_contract = self.place_of_contract_input.text()
            car_cost = self.car_cost_input.text()

            new_transaction = Transaction(buyer, seller, car_info, date, place_of_contract, car_cost)

            try:
                insert_query = (f"INSERT INTO transaction (buyer, seller, car_info, date, Address, Cost) "
                                f"VALUES ('{new_transaction.buyer}', '{new_transaction.seller}', "
                                f"'{new_transaction.car_info}', '{new_transaction.date}', "
                                f"'{new_transaction.place_of_contract}', '{new_transaction.car_cost}')")
                self.cursor.execute(insert_query)

                self.connection.commit()

                QMessageBox.information(self, 'Транзакция добавлена', 'Транзакция успешно добавлена.')

            except mysql.connector.Error as err:
                print(f"Ошибка: {err}")
                QMessageBox.warning(self, 'Ошибка', f'Ошибка добавления транзакции в базу данных: {err}')

            self.buyer_input.clear()
            self.seller_input.clear()
            self.car_info_input.clear()
            self.date_input.clear()
            self.place_of_contract_input.clear()
            self.car_cost_input.clear()

            self.fetch_transactions_from_database()

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка: {e}')

    def delete_transaction(self):
        try:
            current_item = self.transactions_list.currentItem()

            if current_item is not None:
                index = self.transactions_list.currentRow()

                buyer = self.transactions[index].buyer
                seller = self.transactions[index].seller
                date = self.transactions[index].date

                delete_query = (f"DELETE FROM transaction WHERE buyer = '{buyer}' AND seller = '{seller}' AND "
                                f"date = '{date}'")
                self.cursor.execute(delete_query)

                self.connection.commit()

                QMessageBox.information(self, 'Транзакция удалена', 'Транзакция успешно удалена.')

                self.fetch_transactions_from_database()

            else:
                QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, выберите транзакцию из списка для удаления.')

        except mysql.connector.Error as err:
            print(f"Произошла ошибка: {err}")
            QMessageBox.critical(self, 'Ошибка', f'Ошибка удаления: {eкк}')


class GibddInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.car_cost_input = None
        self.place_of_contract_input = None
        self.car_info_input = None
        self.date_input = None
        self.seller_input = None
        self.buyer_input = None
        self.transactions_list = None
        self.transactions = []
        self.setGeometry(730, 300, 500, 500)
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Transactions"
        )
        self.cursor = self.connection.cursor()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Интерфейс сотрудника-гибдд')

        layout = QVBoxLayout()

        view_transactions_layout = QVBoxLayout()
        self.transactions_list = QListWidget()
        view_transactions_layout.addWidget(QLabel('История транзакций:'))
        view_transactions_layout.addWidget(self.transactions_list)

        add_transaction_layout = QFormLayout()
        self.buyer_input = QLineEdit()
        self.buyer_input.setPlaceholderText("фио")
        self.seller_input = QLineEdit()
        self.seller_input.setPlaceholderText("фио")
        self.car_info_input = QLineEdit()
        self.car_info_input.setPlaceholderText("марка")
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("гггг-мм-дд")
        self.place_of_contract_input = QLineEdit()
        self.place_of_contract_input.setPlaceholderText("адрес")
        self.car_cost_input = QLineEdit()
        self.car_cost_input.setPlaceholderText("р.")

        add_transaction_button = QPushButton('Добавить транзакцию')
        add_transaction_button.clicked.connect(self.add_transaction)

        add_transaction_layout.addRow('Покупатель:', self.buyer_input)
        add_transaction_layout.addRow('Продавец:', self.seller_input)
        add_transaction_layout.addRow('Марка авто:', self.car_info_input)
        add_transaction_layout.addRow('Дата транзакции:', self.date_input)
        add_transaction_layout.addRow('Место подписания договора:', self.place_of_contract_input)
        add_transaction_layout.addRow('Стоимость:', self.car_cost_input)
        add_transaction_layout.addWidget(add_transaction_button)

        layout.addLayout(add_transaction_layout)
        layout.addLayout(view_transactions_layout)
        self.setLayout(layout)

        self.fetch_transactions_from_database()

    def fetch_transactions_from_database(self):
        try:
            self.transactions = []
            select_query = "SELECT buyer, seller, car_info, date, Address, Cost FROM transaction"
            self.cursor.execute(select_query)

            rows = self.cursor.fetchall()

            for row in rows:
                buyer, seller, car_info, date, place_of_contract, car_cost = row
                transaction = Transaction(buyer, seller, car_info, date, place_of_contract, car_cost)
                self.transactions.append(transaction)

            self.update_transactions_list()

        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")
            QMessageBox.warning(self, 'Ошибка', f'Ошибка импорта транзакций из базы данных: {err}')

    def update_transactions_list(self):
        self.transactions_list.clear()
        for transaction in self.transactions:
            self.transactions_list.addItem(f'Покупатель: {transaction.buyer}, '
                                           f'Продавец: {transaction.seller}, '
                                           f'Марка авто: {transaction.car_info}, '
                                           f'Дата транзакции: {transaction.date}, '
                                           f'Место подписания договора: {transaction.place_of_contract}, '
                                           f'Стоимость: {transaction.car_cost}')

    def add_transaction(self):
        try:
            buyer = self.buyer_input.text()
            seller = self.seller_input.text()
            car_info = self.car_info_input.text()
            date = self.date_input.text()
            place_of_contract = self.place_of_contract_input.text()
            car_cost = self.car_cost_input.text()

            new_transaction = Transaction(buyer, seller, car_info, date, place_of_contract, car_cost)

            try:
                insert_query = (f"INSERT INTO transaction (buyer, seller, car_info, date, Address, Cost) "
                                f"VALUES ('{new_transaction.buyer}', '{new_transaction.seller}', "
                                f"'{new_transaction.car_info}', '{new_transaction.date}', "
                                f"'{new_transaction.place_of_contract}', '{new_transaction.car_cost}')")
                self.cursor.execute(insert_query)

                self.connection.commit()

                QMessageBox.information(self, 'Транзакция добавлена', 'Транзакция успешно добавлена.')

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                QMessageBox.warning(self, 'Error', f'Error adding transaction to the database: {err}')

            self.buyer_input.clear()
            self.seller_input.clear()
            self.car_info_input.clear()
            self.date_input.clear()
            self.place_of_contract_input.clear()
            self.car_cost_input.clear()

            self.fetch_transactions_from_database()

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка: {e}')
