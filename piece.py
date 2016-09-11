from abc import ABCMeta, abstractmethod
from enum import Enum

class Piece(metaclass=ABCMeta):

    class Color(Enum):
        WHITE = 0 #Player 0 is WHITE
        BLACK = 1 #Player 1 is BLACK
        NONE  = 2 #For empty spaces

    """Abstract base class describing a piece"""

    def __init__(self, color = Color.NONE):
        self.color = color

    def get_color(self):
        return self.color

    @abstractmethod
    def get_string(self):
        """Print the appropriate information for a piece"""
        pass

class Empty(Piece):

    def get_string(self):
        return ' '

class King(Piece):

    def __init__(self, color = Piece.Color.NONE):
        super(King, self).__init__(color)
        self.castle_possible = True

    def get_string(self):
        return '♔' if self.color == Piece.Color.WHITE else '♚'

class Queen(Piece):
    def get_string(self):
        return '♕' if self.color == Piece.Color.WHITE else '♛'

class Rook(Piece):
    def __init__(self, color = Piece.Color.NONE):
        super(Rook, self).__init__(color)
        self.castle_possible = True
    def get_string(self):
        return '♖' if self.color == Piece.Color.WHITE else '♜'

class Bishop(Piece):
    def get_string(self):
        return '♗' if self.color == Piece.Color.WHITE else '♝'

class Knight(Piece):
    def get_string(self):
        return '♘' if self.color == Piece.Color.WHITE else '♞'

class Pawn(Piece):
    def __init__(self, color = Piece.Color.NONE):
        super(Pawn, self).__init__(color)
        self.enpassant_possible = True
        self.two_rank_possible = True
        self.two_rank_last = False

    def get_string(self):
        return '♙' if self.color == Piece.Color.WHITE else '♟'
