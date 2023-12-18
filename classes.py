import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QCloseEvent
from PyQt6.QtCore import Qt
import mysql.connector


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
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
        self.setWindowTitle('Интерфейс пользователя')

        layout = QVBoxLayout()

        # Просмотреть транзакции
        view_transactions_layout = QVBoxLayout()
        self.transactions_list = QListWidget()
        view_transactions_layout.addWidget(QLabel('История транзакций:'))
        view_transactions_layout.addWidget(self.transactions_list)

        layout.addLayout(view_transactions_layout)

        self.setLayout(layout)

        self.fetch_transactions_from_database()

    def fetch_transactions_from_database(self):
        try:
            # Выполните SQL-запрос для выборки транзакций из базы данных
            select_query = "SELECT buyer, seller, car_info, date, Address, Cost FROM transaction"
            self.cursor.execute(select_query)

            # Получите все строки результата
            rows = self.cursor.fetchall()

            # Преобразуйте каждую строку в объект Transaction и добавьте в список
            for row in rows:
                buyer, seller, car_info, date, place_of_contract, car_cost = row
                transaction = Transaction(buyer, seller, car_info, date, place_of_contract, car_cost)
                self.transactions.append(transaction)

            self.update_transactions_list()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            QMessageBox.warning(self, 'Error', f'Error fetching transactions from the database: {err}')

    def update_transactions_list(self):
        self.transactions_list.clear()
        for transaction in self.transactions:
            self.transactions_list.addItem(f'Покупатель: {transaction.buyer}, '
                                           f'Продавец: {transaction.seller}, '
                                           f'Марка: {transaction.car_info}, '
                                           f'Дата: {transaction.date}, '
                                           f'Место подписания договора: {transaction.place_of_contract}, '
                                           f'Стоимость: {transaction.car_cost}')


class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class Transaction:
    def __init__(self, buyer='', seller='', car_info='', date='', place_of_contract='', car_cost=''):
        self.buyer = buyer
        self.seller = seller
        self.car_info = car_info
        self.date = date
        self.place_of_contract = place_of_contract
        self.car_cost = car_cost
