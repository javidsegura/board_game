from PySide6.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy
class GridLogic:
    def __init__(self, grid_size : int, on_cell_click : callable) -> None:
        """
        Parameters:
            - grid_size: int
            - on_button_click: function
        """
        self.grid_size = grid_size
        self.cells = {} # Set of all cells in the grid
        self.on_cell_click = on_cell_click # function to call when ...

    def setup_grid(self) -> QVBoxLayout:
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)  # Spacing between cells

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = QPushButton("")
                cell.setFixedSize(120, 120)
                cell.clicked.connect(lambda _, r=row, c=col: self.on_cell_click(r, c))
                self.grid_layout.addWidget(cell, row, col)
                self.cells[(row, col)] = cell

        grid_container = QVBoxLayout()
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        grid_container.addLayout(self.grid_layout)
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        return grid_container
        
    def disable_grid(self, disable: bool) -> None:
        for cell in self.cells.values():
            cell.setDisabled(disable)

    def reset_buttons(self) -> None:
        """ Reset the grid to its initial state for a new game
        
        TOdo: create a condition to only execute if not already empty"""
        for cell in self.cells.values():
            cell.setText("") # Eliminate icons
            cell.setEnabled(True) # Enable to click on the cell
            cell.setStyleSheet("") # Reset style to default version

    def set_button_state(self, row:int, col:int, text:str, style:str) -> None:
        """ Changes the text and style of a cell """
        self.cells[(row, col)].setText(text)
        self.cells[(row, col)].setStyleSheet(style)

    def disable_button(self, row:int, col:int) -> None:
        self.cells[(row, col)].setDisabled(True)