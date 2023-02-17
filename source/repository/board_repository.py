from constants.constants import BOARD_LENGTH, EMPTY, BOARD_WIDTH


class GameBoard:
    def __init__(self, piece_validator):
        self.__board = [[EMPTY for _ in range(BOARD_LENGTH)] for _ in range(BOARD_WIDTH)]
        self.__number_of_pieces = 0
        self.__piece_validator = piece_validator

    @property
    def board(self):
        return self.__board

    @property
    def number_of_pieces(self):
        return self.__number_of_pieces

    def get_column(self, column_index):
        return [row[column_index] for row in self.board]

    def get_row(self, row_index):
        return self.board[row_index]

    def place_piece(self, piece):
        self.__piece_validator.validate(piece)
        self.__board[piece.row][piece.column] = piece.player_id
        self.__number_of_pieces += 1

    def remove_piece(self, piece):
        self.__piece_validator.validate(piece)
        self.__board[piece.row][piece.column] = EMPTY
        self.__number_of_pieces -= 1
