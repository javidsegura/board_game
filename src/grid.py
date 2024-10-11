from PySide6.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy

class GridLogic:
    def __init__(self, grid_size : int, on_button_click : callable) -> None:
        """
        Parameters:
            - grid_size: int
            - on_button_click: function
        """
        self.grid_size = grid_size
        self.buttons = {}
        self.on_button_click = on_button_click

    def setup_grid(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)  # Spacing between cells

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                btn = QPushButton("")
                btn.setFixedSize(120, 120)
                btn.clicked.connect(lambda _, r=row, c=col: self.on_button_click(r, c))
                self.grid_layout.addWidget(btn, row, col)
                self.buttons[(row, col)] = btn

        grid_container = QVBoxLayout()
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        grid_container.addLayout(self.grid_layout)
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        return grid_container

    def disable_grid(self, disable=True):
        for btn in self.buttons.values():
            btn.setDisabled(disable)

    def reset_buttons(self):
        for btn in self.buttons.values():
            btn.setText("")
            btn.setEnabled(True)
            btn.setStyleSheet("")

    def set_button_state(self, row, col, text, style):
        self.buttons[(row, col)].setText(text)
        self.buttons[(row, col)].setStyleSheet(style)

    def disable_button(self, row, col):
        self.buttons[(row, col)].setDisabled(True)
