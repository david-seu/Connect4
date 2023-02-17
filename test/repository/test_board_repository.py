from source.repository.board_repository import GameBoard
from source.domain.entities import Piece
from source.domain.validators import PieceValidator
from unittest import TestCase
EMPTY = 0
PLAYER_ID = 1
PIECE_ROW = 1
PIECE_COLUMN = 1
BOARD_LENGTH = 7
BOARD_WIDTH = 6
SECOND_ROW = 1
SECOND_COLUMN = 1


class TestBoardRepository(TestCase):

    def setUp(self):
        self.piece_validator = PieceValidator()
        self.board_repository = GameBoard(self.piece_validator)
        self.board = [[EMPTY for _ in range(BOARD_LENGTH)] for _ in range(BOARD_WIDTH)]
        self.board[SECOND_ROW][SECOND_COLUMN] = PLAYER_ID
        self.piece = Piece(PLAYER_ID, PIECE_COLUMN, PIECE_ROW)
        self.column = [EMPTY for _ in range(BOARD_WIDTH)]
        self.row = [EMPTY for _ in range(BOARD_LENGTH)]

    def test_get_column(self):
        self.assertEqual(self.board_repository.get_column(SECOND_COLUMN), self.column)

    def test_get_row(self):
        self.assertEqual(self.board_repository.get_row(SECOND_ROW), self.row)

    def test_place_piece(self):
        self.board_repository.place_piece(self.piece)
        self.assertEqual(self.board_repository.number_of_pieces, 1)

    def test_remove_piece(self):
        self.board_repository.place_piece(self.piece)
        self.board_repository.remove_piece(self.piece)
        self.assertEqual(self.board_repository.number_of_pieces, 0)



