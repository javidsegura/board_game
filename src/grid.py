from PySide6.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy
import os 
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QGridLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt

class GridLogic:
    def __init__(self, grid_size, on_cell_click):
        self.grid_size = grid_size
        self.on_cell_click = on_cell_click
        self.buttons = []

    def setup_grid(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = QPushButton()
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setMinimumSize(50, 50)  # Set a minimum size for the buttons
                button.clicked.connect(lambda _, r=row, c=col: self.on_cell_click(r, c))
                grid_layout.addWidget(button, row, col)
                self.buttons.append(button)

        return grid_layout


    def disable_grid(self, disable):
        for button in self.buttons:
            button.setDisabled(disable)

    def reset_buttons(self):
        for button in self.buttons:
            button.setStyleSheet("")
            button.setEnabled(True)

    def set_button_state(self, row, col, is_mine, revealed):
        button = self.buttons[row * self.grid_size + col]
        if revealed:
            if is_mine:
                button.setStyleSheet("background-color: red;")
            else:
                button.setStyleSheet("background-color: green;")
        else:
            button.setStyleSheet("background-color: yellow;")

    def disable_button(self, row, col):
        self.buttons[row * self.grid_size + col].setDisabled(True)

    def reveal_cells(self, mines, clicked_cells):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) in mines:
                    self.set_button_state(row, col, True, True)
                elif (row, col) in clicked_cells:
                    self.set_button_state(row, col, False, True)
                else:
                    self.set_button_state(row, col, False, False)

