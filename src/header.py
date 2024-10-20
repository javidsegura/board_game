from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider, QFrame)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont

class Header():
      def __init__(self):
        self.wallet_label = QLabel()
        self.multiplier_label = QLabel()
        self.profit_label = QLabel()

      def setup_header(self) -> QFrame:
        header_layout = QHBoxLayout() # Horizontal layout
        header_frame = QFrame() # Frame to contain the header
        header_frame.setStyleSheet("background-color: gray; color: white; border-radius: 5px;")
        header_frame.setLayout(header_layout)

        # Game name
        game_name_label = QLabel("CasinoMines")
        game_name_label.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(game_name_label)

        # Spacer
        header_layout.addStretch()

        # Wallet balance
        self.wallet_label.setText("Balance: 1000$")
        header_layout.addWidget(self.wallet_label)

        # Spacer
        header_layout.addSpacing(20)

        # Current multiplier
        self.multiplier_label.setText("Multiplier: 1x")
        header_layout.addWidget(self.multiplier_label)

        # Profit
        self.profit_label.setText("Profit: 0$")
        header_layout.addWidget(self.profit_label)

        return header_frame
      
      def update_balance(self, new_balance):
        self.wallet_label.setText(f"Balance: {new_balance}$")

      def update_multiplier(self, new_multiplier):
        self.multiplier_label.setText(f"Multiplier: {new_multiplier}x")

      def update_profit(self, new_profit):
        print(f"Profit is {new_profit}")
        # self.profit = new_profit
        self.profit_label.setText(f"Profit: {round(new_profit,2)}$")
