
from multiplier import MultiplierFunc

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