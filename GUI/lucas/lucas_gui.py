import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QSpacerItem, QSizePolicy, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class MinefieldGame(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_size = 5
        self.num_mines = 3
        self.bet_amount_value = 0
        self.buttons = {}
        self.mines = set()

        # Set up the main UI window
        self.setWindowTitle("Modern Minefield Game")
        self.setGeometry(100, 100, 1000, 700)  # Make window larger
        self.setStyleSheet(self.get_stylesheet())

        # Set up the main layout
        self.main_layout = QHBoxLayout()  # Horizontal layout for control panel and game area
        self.setLayout(self.main_layout)

        # Setup the control panel
        self.setup_controls()

        # Setup the game grid
        self.setup_grid()

        self.show()

    def get_stylesheet(self):
        return """
            QWidget {
                background-color: #2b2b2b;
                font-family: Arial;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
            QLineEdit {
                background-color: #444444;
                color: white;
                font-size: 18px;
                padding: 5px;
                border: 2px solid #555555;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #ffcc00;
            }
            QPushButton {
                background-color: #444444;
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton#startButton {
                background-color: #ffcc00;
                color: black;
                font-size: 18px;
            }
            QPushButton#startButton:hover {
                background-color: #ffd633;
            }
            QPushButton:disabled {
                background-color: #888888;
                color: #aaaaaa;
            }
        """

    def setup_controls(self):
        control_layout = QVBoxLayout()

        # Bet label and input field
        self.bet_label = QLabel("Bet Amount: ")
        control_layout.addWidget(self.bet_label)

        self.bet_input = QLineEdit()
        self.bet_input.setPlaceholderText("$0")
        control_layout.addWidget(self.bet_input)

        # Mines label and input field
        self.mines_label = QLabel("Number of Mines: ")
        control_layout.addWidget(self.mines_label)

        self.mines_input = QLineEdit()
        self.mines_input.setPlaceholderText("3")
        control_layout.addWidget(self.mines_input)

        # Add spacing
        control_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Start button
        self.start_button = QPushButton("Start Game")
        self.start_button.setObjectName("startButton")  # Set object name for specific styling
        self.start_button.clicked.connect(self.start_game)
        control_layout.addWidget(self.start_button)

        # Add spacing below button
        control_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add control layout to main layout (on the left)
        self.main_layout.addLayout(control_layout)

    def setup_grid(self):
        # Create a grid for the minefield buttons
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                btn = QPushButton("")
                btn.setFixedSize(120, 120)  # Increase button size
                btn.clicked.connect(lambda _, r=row, c=col: self.on_button_click(r, c))
                self.grid_layout.addWidget(btn, row, col)
                self.buttons[(row, col)] = btn

        # Add grid to main layout, centered
        grid_container = QVBoxLayout()
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        grid_container.addLayout(self.grid_layout)
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.main_layout.addLayout(grid_container)

    def create_minefield(self):
        # Reset the minefield
        for btn in self.buttons.values():
            btn.setText("")
            btn.setEnabled(True)
            btn.setStyleSheet("")

        # Reset the mines set
        self.mines.clear()

        # Randomly place the mines
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            self.mines.add((row, col))


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinefieldGame()
    sys.exit(app.exec())



"""
GPT converstaion explining: https://chatgpt.com/share/66ffc74c-2330-8010-8f19-c425267f7a96

"""