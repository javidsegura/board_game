"""
This module should serve as a general control of the GUI.

It should mainly be reduced to function calls to other modules.

"""

import sys,os, json

from time import sleep

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider, QFrame, QMessageBox)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont


from game_css import GameStyle
from bombs import BombsLogic
from grid import GridLogic
from multiplier import MultiplierFunc
from wallet import Wallet
from configuration_panel import ConfigurationPanel
from header import Header

    

class CasinoMines(QWidget, GameStyle):
    """ Controls the main window of the game"""
    def __init__(self):
        super().__init__()
        self.grid_size = 5
        self.bombs_logic = BombsLogic(self.grid_size)
        self.grid_logic = GridLogic(self.grid_size, self.on_cell_click)
        self.config_panel = ConfigurationPanel()
        self.wallet = Wallet()
        self.header = Header()
        self.first_game = True
        self.game_in_progress = False
        self.clicked_cells = set()
        
    
        # Set up the main UI window
        self.setWindowTitle("CasinoMines Game")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(GameStyle().get_stylesheet())

        # Create the main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)


        # Setup the configuration panel
        self.main_layout.addWidget(self.config_panel.header_element())
        
        self.game_layout = QHBoxLayout()
        self.main_layout.addLayout(self.game_layout)

        self.configuration_panel()

        # Setup the game grid
        self.game_layout.addLayout(self.grid_logic.setup_grid()) 
        self.grid_logic.disable_grid(True)  # Initially disable the grid

        self.show()

    def configuration_panel(self) -> None:
        """ Defines left-most menu. Try to move this to its own file."""

        left_layout, self.cash_out_button= self.config_panel.set_up_panel()

        # Start button is added from here to avoid circular import (it needs to call start_game)
        self.start_button = QPushButton("Start Game")
        self.start_button.setObjectName("startButton")  # Set object name for specific styling
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setDisabled(True)
        left_layout.addWidget(self.start_button)
        self.game_layout.addLayout(left_layout)

        self.config_panel.set_start_button(self.start_button)


    def start_game(self):
        """Function executed when the user clicks on the start button"""
        self.num_mines = self.config_panel.get_num_mines()
        self.create_minefield()
        self.start_button.setDisabled(False) # Disable start button
        self.grid_logic.disable_grid(False) # Activate the grid
        self.game_in_progress = True
        self.config_panel.reset_for_new_game()


    def create_minefield(self) -> None:
        """Create set of mines in the grid"""
        self.grid_logic.reset_buttons() # Reset the grid
        self.bombs_logic.get_mines_set(self.num_mines) # Create set of mines

    def on_cell_click(self, row:int, col:int) -> None:
        """Function executed when the user clicks on a cell"""
        self.clicked_cells.add((row, col))
        if not self.game_in_progress:
            return
        if self.bombs_logic.is_mine(row, col):
            self.grid_logic.set_button_state(row, col, "💣", "background-color: red; font-size: 24px;")
            self.game_over()
        else:
            self.grid_logic.set_button_state(row, col, "⭐️", "background-color: #f2f230; font-size: 24px;")
            self.grid_logic.disable_button(row, col)
            self.config_panel.update_multiplier()
            self.config_panel.update_profit()
            

    def game_over(self):
        """ Defines behavior after user clicked on a cell with a mine"""
        self.game_in_progress = False
        # Showing all other mines
        mines_set = self.bombs_logic.set_of_mines()
        for row, col in self.grid_logic.cells:
            if (row, col) in mines_set:
                self.grid_logic.set_button_state(row, col, "💣", "background-color: red; font-size: 24px;")
            else:
                self.grid_logic.set_button_state(row, col, "⭐️", "background-color: #f2f230; font-size: 24px;")

       # Deactivate corresponding widgets of the GUI
        self.grid_logic.disable_grid(True)

        self.show_GameOver_screen()

    
    def show_GameOver_screen(self):
        """ Shows a game over pop-up and resets the game when dismissed """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText("You hit a mine! Game Over.")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.button(QMessageBox.Ok).setText("Dismiss")
        
        # Connect the buttonClicked signal to our reset function
        msg_box.buttonClicked.connect(self.reset_game_after_popup)
        
        msg_box.exec()

    def reset_game_after_popup(self):
        """ Resets the game after the pop-up is dismissed """
        self.config_panel.activate_btns()
        self.start_button.setDisabled(False)
        self.config_panel.reset_bet()
        self.wallet.reset_bet()
        self.reset_game()

    def reset_game(self):
        """Reset the game state"""
        self.game_in_progress = False
        self.grid_logic.reset_buttons()
        self.config_panel.reset_for_new_game()
        self.start_button.setDisabled(True)
        self.grid_logic.disable_grid(True)








if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CasinoMines()
    sys.exit(app.exec())


