from piece import *
from colorama import Fore, Back, Style
import sys

class Chess:

    def __init__(self):
        #White goes first
        self.current_player = Piece.Color.WHITE
        #Create the board
        self.board = []
        #Top is black
        self.board.append([Rook(Piece.Color.BLACK), Knight(Piece.Color.BLACK), Bishop(Piece.Color.BLACK), Queen(Piece.Color.BLACK), King(Piece.Color.BLACK), Bishop(Piece.Color.BLACK), Knight(Piece.Color.BLACK), Rook(Piece.Color.BLACK)])
        self.board.append([Pawn(Piece.Color.BLACK) for _ in range(8)])
        for __ in range(4): self.board.append([Empty() for _ in range(8)])
        self.board.append([Pawn(Piece.Color.WHITE) for _ in range(8)])
        self.board.append([Rook(Piece.Color.WHITE), Knight(Piece.Color.WHITE), Bishop(Piece.Color.WHITE), Queen(Piece.Color.WHITE), King(Piece.Color.WHITE), Bishop(Piece.Color.WHITE), Knight(Piece.Color.WHITE), Rook(Piece.Color.WHITE)])
        print('Board initialized')

    def print(self):
        row_start_color = Piece.Color.BLACK
        for i in range(8):
            row_start_color = self.swap_color(row_start_color)
            space_color = row_start_color
            for j in range(8):
                space = Back.YELLOW if space_color == Piece.Color.BLACK else Back.WHITE
                print(space + Fore.BLACK + self.board[i][j].get_string() , end='')
                space_color = self.swap_color(space_color)
            print(Back.RESET + Fore.RESET)

    def swap_color(self, color):
        return Piece.Color.BLACK if color == Piece.Color.WHITE else Piece.Color.WHITE
