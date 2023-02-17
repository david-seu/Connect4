from unittest import TestCase
from source.domain.entities import Piece


class TestPiece(TestCase):

    def setUp(self):
        self.piece = Piece(16, 5, 3)

    def test_piece_player_id(self):
        self.assertEqual(self.piece.player_id, 16)

    def test_piece_row(self):
        self.assertEqual(self.piece.row, 3)

    def test_piece_column(self):
        self.assertEqual(self.piece.column, 5)


