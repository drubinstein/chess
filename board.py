from piece import *
from colorama import Fore, Back, Style
import sys

class Chess:

    class ErrorCodes(Enum):
        NONE = 0 #No error
        INVALID_MOVE_LENGTH          = 1 # The string used to make the move is of an invalid length
        OUT_OF_BOUNDS_START_LOCATION = 2 # The string used to denote the start is out of bounds
        OUT_OF_BOUNDS_END_LOCATION   = 3 # The string used to denote the end is out of bounds
        INVALID_PIECE                = 4 # The piece you want to move is invalid
        INVALID_MOVE                 = 5 # The move breaks the rules for the piece

    class BoardStates(Enum):
        NEUTRAL = 0
        WHITE_CHECK = 1 #White is in check
        WHITE_MATE  = 2 #White is mated
        BLACK_CHECK = 3 #Black is in check
        BLACK_MATE  = 4 #Black is mated

    def __init__(self):
        #TODO: Consider allowing custom board positions for different chess variants
        #This could be in the form of the user specifying a specific board layout or having predefined arguments
        #White goes first
        self.current_player = Piece.Color.WHITE
        self.board_state = self.BoardStates.NEUTRAL
        #Create the board
        self.board = []
        #Top is black
        self.board.append([Rook(Piece.Color.BLACK)   \
                         , Knight(Piece.Color.BLACK) \
                         , Bishop(Piece.Color.BLACK) \
                         , Queen(Piece.Color.BLACK)  \
                         , King(Piece.Color.BLACK)   \
                         , Bishop(Piece.Color.BLACK) \
                         , Knight(Piece.Color.BLACK) \
                         , Rook(Piece.Color.BLACK)])
        #row of black pawns
        self.board.append([Pawn(Piece.Color.BLACK) for _ in range(8)])
        #4 empty rows
        for __ in range(4): self.board.append([Empty() for _ in range(8)])
        #row of white pawns
        self.board.append([Pawn(Piece.Color.WHITE) for _ in range(8)])
        #Bottom row
        self.board.append([Rook(Piece.Color.WHITE)   \
                         , Knight(Piece.Color.WHITE) \
                         , Bishop(Piece.Color.WHITE) \
                         , Queen(Piece.Color.WHITE)  \
                         , King(Piece.Color.WHITE)   \
                         , Bishop(Piece.Color.WHITE) \
                         , Knight(Piece.Color.WHITE) \
                         , Rook(Piece.Color.WHITE)])

    def print(self):
        """Print the current board to terminal"""

        #Print the letters
        print(' ', end='')
        for a in range(ord('a'), ord('h')+1): print(chr(a),end='')
        print()

        row_start_color = Piece.Color.BLACK
        for i in range(8):
            row_start_color = self.swap_color(row_start_color)
            space_color = row_start_color

            n_space = str(8 - i )

            print(n_space, end='')
            for j in range(8):
                space = Back.YELLOW if space_color == Piece.Color.BLACK else Back.WHITE
                print(space + Fore.BLACK + self.board[i][j].get_string() , end='')
                space_color = self.swap_color(space_color)
            print(Back.RESET + Fore.RESET + n_space)

        #Print the letters
        print(' ', end='')
        for a in range(ord('a'), ord('h')+1): print(chr(a),end='')
        print()

    def swap_color(self, color):
        return Piece.Color.BLACK if color == Piece.Color.WHITE else Piece.Color.WHITE

    def swap_player(self):
        self.current_player = Piece.Color.WHITE if self.current_player == Piece.Color.BLACK else Piece.Color.White

    def make_move(self, move):
        """Move is a 4 character string representing the start and end location
           For example e2e4 means move the piece at e2 to e4"""

        #First parse the move into the current board position
        src, dest, err = parse_move(move)

        if err != ErrorCodes.NONE:
            return err

        #Now attempt to make the move
        #Check if the piece is the correct color
        sp = self.board[src[0]][src[1]]
        dp = self.board[dest[0]][dest[1]]
        #This works because we have the concept of a colorless empty piece
        if sp.get_color() != self.current_player:
            return ErrorCodes.INVALID_PIECE

        if dp.get_color() == self.current_player:
            return ErrorCodes.INVALID_MOVE

        old_board = self.board
        err = check_move(p, src, dest)

        if err != ErrorCodes.NONE:
            return err

        #Sanity check on putting yourself in check...
        err = check_check()
        if err != ErrorCodes.NONE:
            self.board = old_board
            return err

        #We have finished the move sequence swap players
        swap_player()

        return ErrorCodes.NONE

    def parse_move(self, move):
        if len(move) != 4:
            return 0,0,ErrorCodes.INVALID_MOVE_LENGTH

        #The first letter is between a and h
        #The second character is a number between 1 and 8
        #Because the board here is represented flipped, we have to also add 7
        src = (move[0]-'a', move[1]-'1'+7)
        dest = (move[2]-'a', move[3]-'1'+7)

        #Check validity of the move locations
        if not all(i >= 0 and i <8 for i in src):
            return 0,0,ErrorCodes.OUT_OF_BOUNDS_START_LOCATION

        if not all(i >= 0 and i <8 for i in dest) or src == dest:
            return 0,0,ErrorCodes.OUT_OF_BOUNDS_END_LOCATION

        return src, dest, ErrorCodes.NONE

    def check_check(self):
        pass

    #All check move functions are overloaded for the piece being checked
    """Given the piece, start and end point check, return whether or not the move is valid
    Src and dest are expected to be valid board locations and the src location is expected to be
    a valid starting piece and the end location is assumed to be either a different color or empty"""

    #TODO: Move the piece moving mechanism to the make move function
    #This may not be possible without having other returns to allow for moves like castle and en passant
    #Sigh...castle and en passant

    def check_move(self, p : Rook, src, dest):
        #check to see if one axis is constant between src and dest
        #then check to see there are no pieces in the way
        if src[0] == dest[0]:
            incr = (0,1) if src[1] < dest[1] else (0,-1)
        elif src[1] == dest[1]:
            incr = (1,0) if src[0] < dest[0] else (-1,0)
        else:
            return ErrorCodes.INVALID_MOVE

        #Now iterate from the src to the dest using the increment operator and make sure nothing is blocking.
        tmp = src
        while tmp != dest:
            tmp += incr
            if self.board[tmp[0]][tmp[1]].get_color() != Piece.Color.NONE:
                break
        if tmp != dest:
            return ErrorCodes.INVALID_MOVE

        self.board[dest[0]][dest[1]] = p
        self.board[src[0]][src[1]] = Empty()

        return ErrorCodes.NONE

    def check_move(self, p : Bishop, src, dest):
        #check to make sure the slope is either 1 or -1
        num = src[0] - dest[0]
        denom = src[1] - dest[1]
        if not (num == denom or num == -denom):
            return ErrorCodes.INVALID_MOVE

        #we increment by some combination of 1 and -1 given the slope
        incr = (1 if num > 0 else -1 , 1 if denom > 0 else -1)

        #Now iterate from the src to the dest using the increment operator and make sure nothing is blocking.
        tmp = src
        while tmp != dest:
            tmp += incr
            if self.board[tmp[0]][tmp[1]].get_color() != Piece.Color.NONE:
                break
        if tmp != dest:
            return ErrorCodes.INVALID_MOVE

        self.board[dest[0]][dest[1]] = p
        self.board[src[0]][src[1]] = Empty()

        return ErrorCodes.NONE

    def check_move(self, p : Queen, src, dest):
        old_board = self.board

        if check_move(Bishop(self.current_player), src, dest) == ErrorCodes.None:
            self.board[dest[0][dest[1]] = p
            return ErrorCodes.NONE

        self.board = old_board
        if check_move(Rook(self.current_player, castle_possible=False), src, dest) == ErrorCodes.None:
            self.board[dest[0][dest[1]] = p
            return ErrorCodes.NONE

        return ErrorCodes.INVALID_MOVE

    def check_move(self, p: Knight, src, dest):
        #check to see if the destination is either (+-1,+-2) or (+-2, +-1) away
        dy = src[0] - dest[0]
        dx = src[1] - dest[1]
        poss = [-1, 1, -2, 2]
        if not ((dx in poss) and (dy in poss) and (dx != dy)):
            return ErrorCodes.INVALID_MOVE

        self.board[dest[0]][dest[1]] = p
        self.board[src[0]][src[1]] = Empty()

        return ErrorCodes.NONE

    def check_move(self, p: King, src, dest):

        #first check if the move is a castle
        """
        old_board = self.board
        if p.castle_possible:
            #if moving left check if there's a rook in the left corner
            #if moving right check if there's a rook on the right side
            if dest[1] - src[1] == -2: #moving left
                if type(self.board[src[0]][0]) == type(Rook) and self.board[src[0]][0].castle_possible == True:
                    #move the king towards the spot checking for check each time



            if dest[1] - src[1] == 2: #moving right
                if type(self.board[src[0]][7]) == type(Rook) and self.board[src[0]][7].castle_possible == True:
        """

        #now check to see if the move is possible otherwise
        dy = dest[0] - src[0]
        dx = dest[1] - src[1]
        if not (dy in [1,-1] and dx in [1,-1]):
            return ErrorCodes.NONE

        self.board[dest[0]][dest[1]] = p
        self.board[src[0]][src[1]] = Empty()

    def check_move(self, p: Pawn, src, dest):
        if p.two_rank_possible and src[1] == dest[1] and (dest[0] - src[0] in [2,-2]):

            #perform a two rank move


