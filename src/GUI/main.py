"""
This module should serve as a general control of the GUI.

It should mainly be reduced to function calls to other modules.

"""

import sys,os

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider)
from PySide6.QtCore import QTimer, Qt

from game_css import GameStyle
from bombs import BombsLogic
from grid import GridLogic
from multiplier import MultiplierFunc
from wallet import Wallet



class RoobetMines(QWidget, GameStyle):
    def __init__(self):
        super().__init__()
        self.grid_size = 5
        self.bombs_logic = BombsLogic(self.grid_size)
        self.grid_logic = GridLogic(self.grid_size, self.on_button_click)
        self.wallet = Wallet()  # Initialize the wallet
        self.current_bet = 0
        self.current_multiplier = 1
        self.current_profit = 0

        # Set up the main UI window
        self.setWindowTitle("Modern Minefield Game")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(GameStyle().get_stylesheet())

        # Start the main layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Start the control panel
        self.configuration_panel()

        # Setup the game grid
        self.main_layout.addLayout(self.grid_logic.setup_grid())
        self.grid_logic.disable_grid(True)  # Initially disable the grid

        # Setup the wallet and multiplier display
        self.setup_wallet_display()

        self.show()

    def setup_wallet_display(self):
        wallet_layout = QVBoxLayout()

        self.wallet_label = QLabel(f"Wallet: ${self.wallet.get_balance():.2f}")
        wallet_layout.addWidget(self.wallet_label)

        self.multiplier_label = QLabel(f"Multiplier: {self.wallet.get_current_multiplier():.2f}x")
        wallet_layout.addWidget(self.multiplier_label)

        self.profit_label = QLabel("Profit: $0.00")
        wallet_layout.addWidget(self.profit_label)

        self.cashout_button = QPushButton("Cash Out")
        self.cashout_button.clicked.connect(self.cash_out)
        self.cashout_button.setDisabled(True)
        wallet_layout.addWidget(self.cashout_button)

        self.main_layout.addLayout(wallet_layout)
    

    def configuration_panel(self):
        """
        Defines left-most menu
        """
        control_layout = QVBoxLayout()

        # Bet label and input field
        self.bet_label = QLabel("Bet Amount: ")
        control_layout.addWidget(self.bet_label)
        self.bet_input = QLineEdit()
        control_layout.addWidget(self.bet_input)

        # Bet percentage buttons
        bet_percentage_layout = QHBoxLayout()
        percentages = [10, 25, 50, 75, 100]
        for percentage in percentages:
            btn = QPushButton(f"{percentage}%")
            btn.clicked.connect(lambda _, p=percentage: self.set_bet_percentage(p))
            bet_percentage_layout.addWidget(btn)
        control_layout.addLayout(bet_percentage_layout)

        # Mines label and slider
        self.mines_label = QLabel("Number of Mines: 1")
        control_layout.addWidget(self.mines_label)
        self.mines_slider = QSlider(Qt.Horizontal)
        self.mines_slider.setMinimum(1)
        self.mines_slider.setMaximum(24)
        self.mines_slider.setValue(1)
        self.mines_slider.valueChanged.connect(self.update_mines_label)
        control_layout.addWidget(self.mines_slider)

        # Confirm button
        self.confirm_button = QPushButton("Confirm Selection")
        self.confirm_button.clicked.connect(self.confirm_selection)
        control_layout.addWidget(self.confirm_button)

        # Warning label
        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red;")
        control_layout.addWidget(self.warning_label)

        # Start button
        self.start_button = QPushButton("Start Game")
        self.start_button.setObjectName("startButton")  # Set object name for specific styling
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setDisabled(True)  # Disabled initially
        control_layout.addWidget(self.start_button)

        # Add spacing
        control_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # Add spacing below button
        control_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # Add control layout to main layout (on the left)
        self.main_layout.addLayout(control_layout)
    
    def set_bet_percentage(self, percentage):
        bet_amount = self.wallet.calculate_percentage_bet(percentage)
        self.bet_input.setText(f"{bet_amount:.2f}")

    def update_mines_label(self):
        self.mines_label.setText(f"Number of Mines: {self.mines_slider.value()}")

    def create_minefield(self):
        """ Control the bombs
        This should be on a different file
        """
        self.grid_logic.reset_buttons()
        self.bombs_logic.create_minefield(self.num_mines)

    def on_button_click(self, row, col):
        if self.bombs_logic.is_mine(row, col):
            self.grid_logic.set_button_state(row, col, "💣", "background-color: red; font-size: 24px;")
            self.game_over()
        else:
            self.grid_logic.set_button_state(row, col, "⭐️", "background-color: #f2f230; font-size: 24px;")
            self.grid_logic.disable_button(row, col)
            self.update_multiplier()

    def update_multiplier(self):
        try:
            self.current_multiplier = next(self.multiplier_generator)
            self.multiplier_label.setText(f"Multiplier: {self.current_multiplier:.2f}x")
        except StopIteration:
            self.cash_out()
    
    def cash_out(self):
        winnings = self.wallet.cash_out()
        self.update_wallet_display()
        self.game_over()

    def game_over(self):
        for row, col in self.bombs_logic.get_mines():
            self.grid_logic.set_button_state(row, col, "💣", "background-color: red; font-size: 24px;")
        self.grid_logic.disable_grid(True)
        self.cashout_button.setDisabled(True)
        self.start_button.setDisabled(False)
        self.confirm_button.setDisabled(False)
        self.bet_input.setDisabled(False)
        self.mines_slider.setDisabled(False)
        self.multiplier_func.stop_generator()
        self.wallet.reset_bet()
        self.update_wallet_display()
        self.bet_input.setText("")
        

    def update_wallet_display(self):
        self.wallet_label.setText(f"Wallet: ${self.wallet.get_balance():.2f}")

    def update_profit_display(self):
        self.profit_label.setText(f"Profit: ${self.wallet.get_current_profit():.2f}")
    
    def update_multiplier(self):
        try:
            new_multiplier = next(self.multiplier_generator)
            self.wallet.update_multiplier(new_multiplier)
            self.multiplier_label.setText(f"Multiplier: {self.wallet.get_current_multiplier():.2f}x")
            self.update_profit_display()
        except StopIteration:
            self.cash_out()


    def confirm_selection(self):
        try:
            bet_amount = float(self.bet_input.text())
            self.num_mines = self.mines_slider.value()

            if self.num_mines < 1 or self.num_mines >= (self.grid_size ** 2) - 1:
                raise ValueError("Invalid number of mines.")

            if bet_amount > self.wallet.get_balance():
                raise ValueError("Bet amount exceeds wallet balance.")
        
            if bet_amount < 1:
                raise ValueError("Bet amount must be greater than 0.")

            self.wallet.place_bet(bet_amount)
            self.update_wallet_display()
            self.start_button.setDisabled(False)
            self.warning_label.setText("")

        except ValueError as e:
            self.show_warning(str(e))
            self.start_button.setDisabled(True)


    def show_warning(self, message):
        self.warning_label.setText(message)
        QTimer.singleShot(3000, lambda: self.warning_label.setText("")) # Warning is cleared after 3 seconds


    def start_game(self):
        self.create_minefield()
        self.grid_logic.disable_grid(False)
        self.start_button.setDisabled(True)
        self.confirm_button.setDisabled(True)
        self.bet_input.setDisabled(True)
        self.mines_slider.setDisabled(True)
        self.cashout_button.setDisabled(False)

        self.multiplier_func = MultiplierFunc(self.grid_size ** 2, self.num_mines)
        self.multiplier_generator = self.multiplier_func.get_next_multiplier()
        self.update_multiplier()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinefieldGame()
    sys.exit(app.exec())


