import random
import pygame
from Queue import Queue
from tetromino import Tetromino
from constants import SHAPES, WIDTH, GRID_SIZE, BLACK, RED, GAME_OVER_HEIGHT, HEIGHT

class TetrisBoard:
    """
    Manages the game state of a Tetris game, including the grid, current piece,
    score, and game-over condition.
    """

    def __init__(self, width, height):
        """
        Initializes the Tetris board with a specified width and height.

        Args:
            width: The width of the Tetris grid (number of columns).
            height: The height of the Tetris grid (number of rows).
        """
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)] # Initialize an empty grid
        self.game_over = False
        self.score = 0
        self.queue = Queue(self.new_piece())
        for _ in range(5): self.queue.add(self.new_piece())
        self.current_piece = self.queue.next()
        self.swapped = False

    def new_piece(self):
        """
        Generates and returns a new random Tetromino piece at the top-center of the grid.
        """
        shape = random.choice(SHAPES)
        return Tetromino(self.width // 2, 0, shape)

    def valid_move(self, piece, x, y, rotation):
        """
        Checks if moving or rotating the current piece would result in a valid state.

        Args:
            piece: The current Tetromino piece.
            x: The horizontal movement (left/right).
            y: The vertical movement (down).
            rotation: The rotation to apply to the piece.

        Returns:
            True if the move is valid, False otherwise.
        """
        proposed_rotation = (piece.rotation + rotation) % len(piece.shape)
        for i, row in enumerate(piece.shape[proposed_rotation]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    proposed_x = piece.x + j + x
                    proposed_y = piece.y + i + y
                    if not (0 <= proposed_x < self.width) or not (0 <= proposed_y < self.height):
                        return False
                    if self.grid[proposed_y][proposed_x] != 0:
                        return False
        return True
    
    def move(self, dx, dy):
        """
        Attempts to move the current piece by dx and dy units.

        Args:
            dx (int): The change in the x-coordinate (horizontal move).
            dy (int): The change in the y-coordinate (vertical move).

        If the move is valid (i.e., it does not result in a collision or go out of bounds),
        updates the current piece's position accordingly.
        """
        if self.valid_move(self.current_piece, dx, dy, 0):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotateCounterClockWise(self):
        """
        Attempts to rotate the current piece.

        Rotates the piece if the rotation does not result in a collision or
        going out of bounds. The rotation is always clockwise.
        """
        # Calculate the next rotation state (0, 1, 2, 3) in a cyclic manner
        new_rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape)

        # Check if the new rotation would be valid
        if self.valid_move(self.current_piece, 0, 0, 1):
            # Apply the rotation
            self.current_piece.rotation = new_rotation
            return True
        return False
    
    def rotateClockwise(self):
        new_rotation = (self.current_piece.rotation - 1) % len(self.current_piece.shape)
        # Check if the new rotation would be valid
        if self.valid_move(self.current_piece, 0, 0, 1):
            # Apply the rotation
            self.current_piece.rotation = new_rotation
            return True
        return False

    def clear_lines(self):
        """
        Clears completed lines from the grid and updates the score.

        Returns:
            The number of lines cleared.
        """
        lines_cleared = 0
        new_grid = [row for row in self.grid if not all(cell != 0 for cell in row)]
        lines_cleared = self.height - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.width)])
        self.grid = new_grid
        return lines_cleared

    def check_game_over(self):
        """Checks if the game is over, i.e., if any blocks are above the GAME_OVER_HEIGHT."""
        for y in range(GAME_OVER_HEIGHT):
            for x in range(self.width):
                if self.grid[y][x] != 0:  # There's a block above the game over height
                    self.game_over = True
                    return True
        return False
    
    def hold(self):
        if self.swapped:
            return
        self.current_piece.x = self.width//2
        self.current_piece.y = 0
        self.current_piece = self.queue.swap(self.current_piece)
        if self.current_piece == None:
            self.current_piece = self.new_piece()
        self.swapped = True

    def lock_piece(self, piece):
        """
        Locks the current piece into the grid, checks for line clearance,
        updates the score, generates a new piece, and checks for game over.
        """
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    self.grid[piece.y + i][piece.x + j] = piece.color
        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100
        self.current_piece = self.queue.next()
        self.queue.add(self.new_piece())
        self.check_game_over() # Check if the game is over after locking the piece
        self.swapped = False

    def update(self):
        """
        Updates the game state by moving the current piece down one unit,
        locking the piece if necessary, and handling game logic.
        """
        if self.valid_move(self.current_piece, 0, 1, 0):
            self.current_piece.y += 1
        else:
            self.lock_piece(self.current_piece)
    def hardDrop(self):
        while (self.valid_move(self.current_piece, 0, 1, 0)):
            self.current_piece.y += 1
        self.lock_piece(self.current_piece)

        
    def draw_game_over_height(self, screen):
        """
        Draws a horizontal line on the screen indicating the GAME_OVER_HEIGHT.
        """
        line_y = GAME_OVER_HEIGHT * GRID_SIZE
        pygame.draw.line(screen, RED, (0, line_y), (WIDTH, line_y), 2)

    def draw(self, screen):
        """
        Draws the current game state to the screen, including the grid,
        the current piece, and the game over height line.
        """
        screen.fill(BLACK)
        self.draw_game_over_height(screen)
        # Draw each cell in the grid
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
        
        # Draw the current Tetromino
        for i, row in enumerate(self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    pygame.draw.rect(screen, self.current_piece.color, ((self.current_piece.x + j) * GRID_SIZE, (self.current_piece.y + i) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))


class LiteTetrisBoard(TetrisBoard):
    """
    This class manages another gamemode of Tetris named Tetris Lite
    It copies the functionality of the class TetrisBoard but with a smaller board size
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        

    def draw_rectangle(self, screen, x = None, y = GAME_OVER_HEIGHT * GRID_SIZE, width = None, height = None, color = RED):
        if x is None:
            x = self.width * GRID_SIZE
        if width is None:
            width = WIDTH - self.width
        if height is None:
            height = HEIGHT - self.height
        

        pygame.draw.rect(screen, color, (x,y,width, height))
    
    def draw(self, screen):
        """
        Draws the current game state to the screen, including the grid,
        the current piece, and the game over height line.
        """
        screen.fill(BLACK)
        self.draw_game_over_height(screen)
        
        # Draw each cell in the grid
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
        
        # Draw the current Tetromino
        for i, row in enumerate(self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    pygame.draw.rect(screen, self.current_piece.color, ((self.current_piece.x + j) * GRID_SIZE, (self.current_piece.y + i) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
        

        self.draw_rectangle(screen)


class RegularTetrisBoard(TetrisBoard):
    """
    This class manages another gamemode of Tetris named Tetris Lite
    It copies the functionality of the class TetrisBoard but with a smaller board size
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        

    def draw_rectangle(self, screen, x = None, y = GAME_OVER_HEIGHT * GRID_SIZE, width = None, height = None, color = RED):
        if x is None:
            x = self.width * GRID_SIZE
        if width is None:
            width = WIDTH - self.width
        if height is None:
            height = HEIGHT - self.height
        

        pygame.draw.rect(screen, color, (x,y,width, height))
    
    def draw(self, screen):
        """
        Draws the current game state to the screen, including the grid,
        the current piece, and the game over height line.
        """
        screen.fill(BLACK)
        self.draw_game_over_height(screen)
        
        # Draw each cell in the grid
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
        
        # Draw the current Tetromino
        for i, row in enumerate(self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    pygame.draw.rect(screen, self.current_piece.color, ((self.current_piece.x + j) * GRID_SIZE, (self.current_piece.y + i) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
        

        self.draw_rectangle(screen)