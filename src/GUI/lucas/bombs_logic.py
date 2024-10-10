"""
Controls all the logic related to the bombs
"""

import random         
from PySide6.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy

class BombsLogic:
    def __init__(self):
        pass

    def on_button_click(self, row, col):
        if (row, col) in self.mines:
            self.buttons[(row, col)].setText("💣")
            self.buttons[(row, col)].setStyleSheet("background-color: red; font-size: 24px;")
            self.game_over()
        else:
            self.buttons[(row, col)].setText("✔")
            self.buttons[(row, col)].setStyleSheet("background-color: green; font-size: 24px;")
            self.buttons[(row, col)].setDisabled(True)

    def game_over(self):
        for row, col in self.mines:
            self.buttons[(row, col)].setText("💣")
            self.buttons[(row, col)].setStyleSheet("background-color: red; font-size: 24px;")
        for btn in self.buttons.values():
            btn.setDisabled(True)

    def start_game(self):
        try:
            # Read bet amount and number of mines from input fields
            self.bet_amount_value = float(self.bet_input.text())  # Bet amount
            self.num_mines = int(self.mines_input.text())  # Number of mines

            if self.num_mines < 1 or self.num_mines >= self.grid_size ** 2:
                raise ValueError("Invalid number of mines.")

            # Start the game if inputs are valid
            self.create_minefield()
        except ValueError:
            # Handle invalid input by resetting values or displaying an error
            self.bet_input.setText("Invalid Input")
            self.mines_input.setText("Invalid Input")

