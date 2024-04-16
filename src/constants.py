# Screen dimensions
WIDTH, HEIGHT = 450, 600
GRID_SIZE = 25
GAME_OVER_HEIGHT = 4  # Number of rows from the top

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)  # Aqua/cyan color
MAGENTA = (255, 0, 255)  # Magenta/pink color
YELLOW = (255, 255, 0)  # Yellow color
ORANGE = (255, 165, 0)  # Orange color
PURPLE = (128, 0, 128)  # Purple color
LIGHT_GREEN = (144, 238, 144)  # Light green color
LIGHT_BLUE = (173, 216, 230)  # Light blue color

# Update the COLORS list to include these new colors
COLORS = [CYAN, MAGENTA, YELLOW, ORANGE, PURPLE, LIGHT_GREEN, LIGHT_BLUE]

# Tetromino shapes
SHAPES = [
    # I shape
    [
        [".....", ".....", ".....", "OOOO.", "....."],
        [".....", "..O..", "..O..", "..O..", "..O.."],
    ],
    # T Shape
    [
        [".....", ".....", "..O..", ".OOO.", "....."],
        [".....", "..O..", ".OO..", "..O..", "....."],
        [".....", ".....", ".OOO.", "..O..", "....."],
        [".....", "..O..", "..OO.", "..O..", "....."],
    ],
    # Z Shape
    [
        [".....", ".....", ".OO..", "..OO.", "....."],
        [".....", "..O..", ".OO..", ".O...", "....."],
    ],
    # L shape
    [
        [".....", "..O..", "..O.", "..OO..", "....."],
        [".....", "...O.", ".OOO.", ".....", "....."],
        [".....", ".OO..", "..O..", "..O..", "....."],
        [".....", ".....", ".OOO.", ".O...", "....."],
    ],
    # S Shape
    [
        [".....", ".....", "..OO.", ".OO..", "....."],
        [".....", ".O...", ".OO..", "..O..", "....."],
    ],
    # J Shape
    [
        [".....", "..O..", "..O..", ".OO..", "....."],   #["..O.O.."]
        [".....", ".....", ".OOO.", "...O.", "....."],   #["..OOO..."]
        [".....", "..OO.", "..O..", "..O..", "....."],   #["..OO."]
        [".....", ".O....", ".OOO.", ".....", "....."],
    ],
    # Square Shape
    [
        [".....", "..OO.", "..OO.", ".....", "....."]
    ]
]

SCORE_FILE = 'highest_score.txt'