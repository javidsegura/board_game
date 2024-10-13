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

    def place_bet(self, amount):
        self.current_bet = amount
        self.balance -= amount

    def update_multiplier(self, new_multiplier):
        self.current_multiplier = new_multiplier

    def cash_out(self):
        winnings = self.current_bet * self.current_multiplier
        self.balance += winnings
        self.reset_bet()
        return winnings

    def reset_bet(self):
        self.current_bet = 0
        self.current_multiplier = 1

    def get_balance(self):
        return self.balance

    def get_current_bet(self):
        return self.current_bet

    def get_current_multiplier(self):
        return self.current_multiplier

    def calculate_percentage_bet(self, percentage):
        return abs(self.balance) * (percentage / 100)
