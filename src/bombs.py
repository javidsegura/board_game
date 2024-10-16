"""
Controls all the logic related to the bombs
"""

import random

class BombsLogic():
    def __init__(self, grid_size:int) -> None:
        self.grid_size = grid_size
        self.mines = set() # Here we will set the coordinates of the mines

    def get_mines_set(self, num_mines:int) -> None:
        """
        Creates the set with the mines coordinates
        """
        self.num_mines = num_mines
        self.mines.clear() # Remove all elements in the set
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            self.mines.add((row, col))

    def is_mine(self, row:int, col:int) -> bool: 
        """ Determines if the given cell is a mine or not
        --Compute the hash function to increase performance--
        """
        return (row, col) in self.mines

    def set_of_mines(self) -> set:
        """ Returns the set of mines"""
        return self.mines