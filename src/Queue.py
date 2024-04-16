from tetromino import Tetromino
class Queue:
    def __init__(self, piece : Tetromino):
        self.q = [piece]
        self.hold = None

    def next(self) -> Tetromino:
        return(self.q.pop(0))

    def swap(self, piece) -> Tetromino:
        toSwap = self.hold
        self.hold = piece
        return toSwap

    def add(self, piece):
        self.q.append(piece)

    @property
    def currentpiece(self):
        return self.q[0]