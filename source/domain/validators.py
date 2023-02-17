from source.exceptions.exceptions import InvalidColumn


class PieceValidator:

    @staticmethod
    def validate(piece):
        if not 0 <= piece.column <= 7:
            raise InvalidColumn("Column must be between 1 and 7")

