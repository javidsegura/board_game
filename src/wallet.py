from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider)
from PySide6.QtCore import QTimer, Qt

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider)
from PySide6.QtCore import QTimer, Qt

class Wallet:
    def __init__(self, initial_balance=1000):
        """
        Initializes the wallet class
        """
        self.balance = initial_balance # Money in the account
        self.current_bet = 0 # Current bet
        self.current_multiplier = 1 # Current multiplier
        self.profit = 0 # Current profit
        self.prior_profit = 0 # Prior profit
        self.prior_multiplier = 1 # Prior multiplier

    def place_bet(self, amount):
        print(f"Placing bet of {amount}")
        print(f"Placing bet of {amount}")
        self.current_bet = amount
        self.balance -= amount

    def update_multiplier(self, new_multiplier):
        self.current_multiplier = new_multiplier

    def cash_out(self):
        winnings = self.current_bet * self.current_multiplier
        self.balance += winnings
        self.prior_profit = self.calculate_profit()
        self.prior_multiplier = self.current_multiplier
        self.reset_bet()

        return winnings

    def reset_bet(self):
        """ Reset wallet acount values"""
        """ Reset wallet acount values"""
        self.current_bet = 0
        self.current_multiplier = 1
        self.profit = 0
        self.profit = 0

    def get_balance(self):
        return self.balance

    def get_current_bet(self):
        return self.current_bet

    def get_current_multiplier(self):
        return self.current_multiplier

    def calculate_percentage_bet(self, percentage):
        return abs(self.balance) * (percentage / 100)
    
    def calculate_profit(self):
        print(f"Calculating profit: {self.current_bet} * {self.current_multiplier}")
        self.profit = self.current_bet * self.current_multiplier - self.current_bet
        print(f"Profit: {self.profit}\n")
        return self.profit