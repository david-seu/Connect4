from unittest import TestCase
from source.domain.entities import Piece
from source.domain.validators import PieceValidator
from source.exceptions.exceptions import InvalidColumn


class TestValidators(TestCase):

    def setUp(self):
        self.piece_validator = PieceValidator()
        self.piece_invalid_column = Piece(15, 10, 2)

    def test_validate_invalid_column(self):
        self.assertRaises(InvalidColumn, self.piece_validator.validate, self.piece_invalid_column)
