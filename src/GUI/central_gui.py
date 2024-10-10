"""
This module should serve as a general control of the GUI.

It should mainly be reduced to function calls to other modules.

"""

import sys, random
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QSpacerItem, QSizePolicy, QLineEdit
from PySide6.QtCore import QTimer

from game_css import GameStyle
from bombs_logic import BombsLogic # This is where the bomb logic should be. To eventually be moved here.
#from MATH.multiplier import MultiplierFunc

class MinefieldGame(QWidget, GameStyle, BombsLogic):
    def __init__(self):
        """ General control of the GUI"""
        super().__init__()
        self.grid_size = 5 # 5 x 5
        self.buttons = {}
        self.mines = set() # Coordinates of the bombs => Set because we dont wannt duplicated coordinates

        # Set up the main UI window
        self.setWindowTitle("Modern Minefield Game")
        self.setGeometry(100, 100, 1000, 700)  # Make window larger
        self.setStyleSheet(GameStyle().get_stylesheet())

        # Start the main layout
        self.main_layout = QHBoxLayout()  # Horizontal layout for control panel and game area
        self.setLayout(self.main_layout)

        # Start the control panel
        self.configuration_panel()

        # Setup the game grid
        self.setup_grid()
        self.disable_grid(True) # Initially disable the grid

        self.show()
    
    def disable_grid(self, disable=True):
        """
        Initially disable the grid until input is confirmed to be correct
        """
        for btn in self.buttons.values():
            btn.setDisabled(disable)

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

        # Mines label and input field
        self.mines_label = QLabel("Number of Mines: ")
        control_layout.addWidget(self.mines_label)
        self.mines_input = QLineEdit()
        control_layout.addWidget(self.mines_input)

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

    """ 
    **********************************************************************************
        BOMB LOGIC  BELOW HERE => We need to move this section to a different file
    **********************************************************************************
    """

    def setup_grid(self):
        """"
        Defines right mox 
        Note: this is where our algorithims will reside 
        """

        # Create a grid for the minefield buttons
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10) # Spacing between cells

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                btn = QPushButton("")
                btn.setFixedSize(120, 120)  
                btn.clicked.connect(lambda _, r=row, c=col: self.on_button_click(r, c)) # whats this notation?
                self.grid_layout.addWidget(btn, row, col)
                self.buttons[(row, col)] = btn

        # Add grid to main layout, centered
        grid_container = QVBoxLayout()
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        grid_container.addLayout(self.grid_layout)
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.main_layout.addLayout(grid_container)

    def create_minefield(self):
        """ Control the bombs
        This should be on a different file
        """
        # Reset the minefield --> What this doing?
        for btn in self.buttons.values():
            btn.setText("")
            btn.setEnabled(True)
            btn.setStyleSheet("")

        # Reset the mines set
        self.mines.clear() # Coordinates of the bombs

        # Randomly place the mines
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            self.mines.add((row, col))
    
    def on_button_click(self, row, col):
        """
        What happens when you click a button
        """
        # If given cell is a mine
        if (row, col) in self.mines:
            self.buttons[(row, col)].setText("💣")
            self.buttons[(row, col)].setStyleSheet("background-color: red; font-size: 24px;")
            self.game_over()
        else:
            self.buttons[(row, col)].setText("✔")
            self.buttons[(row, col)].setStyleSheet("background-color: green; font-size: 24px;")
            self.buttons[(row, col)].setDisabled(True)

    def game_over(self):
        """
        What happens when you click a mine
        """
        for row, col in self.mines:
            self.buttons[(row, col)].setText("💣")
            self.buttons[(row, col)].setStyleSheet("background-color: red; font-size: 24px;")
        for btn in self.buttons.values():
            btn.setDisabled(True)

    def confirm_selection(self):
        try:
            self.bet_amount_value = float(self.bet_input.text())
            self.num_mines = int(self.mines_input.text())

            if self.num_mines < 1 or self.num_mines >= (self.grid_size ** 2) - 1:
                raise ValueError("Invalid number of mines.")

            self.start_button.setDisabled(False)  # Enable start button
            self.warning_label.setText("")  # Clear any previous warnings

        except ValueError:
            self.show_warning("Invalid input. Please check your bet and mines.")
            self.start_button.setDisabled(True)  # Ensure start button is disabled


    def show_warning(self, message):
        self.warning_label.setText(message)
        QTimer.singleShot(3000, lambda: self.warning_label.setText(""))  # Clear after 3 seconds



    def start_game(self):
        """
        What happens when you click the start button
        """
        self.create_minefield()
        self.disable_grid(False)  # Enable grid
        self.start_button.setDisabled(True)  # Disable start button
        self.confirm_button.setDisabled(True)  # Disable confirm button
        self.bet_input.setDisabled(True)  # Disable bet input
        self.mines_input.setDisabled(True)  # Disable mines input


if __name__ == "__main__":
    app = QApplication(sys.argv) # Initialize the application
    window = MinefieldGame() # Initialize the main window (actual GUI)
    sys.exit(app.exec()) # Start the event loop




