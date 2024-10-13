from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider, QFrame)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from wallet import Wallet

class Header():
      def __init__(self):
        self.wallet = Wallet()
        self.wallet_label = QLabel(f"Balance: ${self.wallet.get_balance():.2f}")
        self.multiplier_label = QLabel("Multiplier: 1.00x")
    
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
        self.wallet_label.setFont(QFont("Arial", 14))
        header_layout.addWidget(self.wallet_label)

        # Spacer
        header_layout.addSpacing(20)

        # Current multiplier
        self.multiplier_label.setFont(QFont("Arial", 14))
        header_layout.addWidget(self.multiplier_label)

        return header_frame
    
      def update_balance(self, new_balance):
        print(new_balance, "  am about to update")
        self.wallet_label.setText(f"Balance: ${new_balance:.2f}")

      def update_multiplier(self, new_multiplier):
        print(new_multiplier, "  am about to update")
        self.multiplier_label.setText(f"Multiplier: {new_multiplier:.2f}x")