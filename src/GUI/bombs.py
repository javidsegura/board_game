"""
Controls all the logic related to the bombs
"""

import random

class BombsLogic():
    def __init__(self, grid_size:int) -> None:
        self.grid_size = grid_size
        self.mines = set()
        self.num_mines = 0 # can this be removed?

    def create_minefield(self, num_mines):
        self.num_mines = num_mines
        self.mines.clear()
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            self.mines.add((row, col))

    def is_mine(self, row, col): # THIS IS WHERE WE IMPLEMENT BORIS' ALGORITHIMS
        return (row, col) in self.mines

    def get_mines(self):
        return self.mines