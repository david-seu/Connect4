from source.service.game_service import GameService, Ai
from source.repository.board_repository import GameBoard
from source.domain.validators import PieceValidator
from source.domain.entities import Piece
from unittest import TestCase
EMPTY = 0
PLAYER_ID = 1
PIECE_ROW = 5
PIECE_COLUMN = 1
BOARD_LENGTH = 7
BOARD_WIDTH = 6
SIXTH_ROW = 5
SECOND_COLUMN = 1


class TestGameService(TestCase):

    def setUp(self):
        self.piece_validator = PieceValidator()
        self.board_repository = GameBoard(self.piece_validator)
        self.game_service = GameService(self.board_repository)
        self.piece = Piece(PLAYER_ID, PIECE_COLUMN, PIECE_ROW)

    def test_get_board(self):
        self.assertEqual(self.game_service.get_board(), self.board_repository.board)

    def test_drop_piece(self):
        piece = self.game_service.drop_piece(PIECE_COLUMN, PLAYER_ID)
        self.assertEqual(piece.player_id, self.piece.player_id)
        self.assertEqual(piece.column, self.piece.column)
        self.assertEqual(piece.row, self.piece.row)
        self.assertEqual(self.board_repository.number_of_pieces, 1)

    def test_is_winning_move(self):
        self.assertEqual(self.game_service.is_winning_move(), None)
