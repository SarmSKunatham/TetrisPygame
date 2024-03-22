import random
from constants import COLORS

class Tetromino:
    """
    Represents a single Tetromino piece in the Tetris game, encapsulating its position,
    shape, color, and rotation state.

    Attributes:
        x (int): The x-coordinate of the Tetromino's position on the Tetris grid.
        y (int): The y-coordinate of the Tetromino's position on the Tetris grid.
        shape (list): A list of strings representing the shape of the Tetromino.
        color (tuple): The RGB color of the Tetromino, randomly chosen from predefined colors.
        rotation (int): The current rotation state of the Tetromino, starting at 0.
    """

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)  # Selects a random color from the COLORS constant.
        self.rotation = 0  # Initializes the rotation state of the Tetromino to 0.
