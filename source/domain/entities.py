

class Piece:

    def __init__(self, player_id, column, row=0):
        self.__player_id = player_id
        self.__column = column
        self.__row = row

    @property
    def player_id(self):
        return self.__player_id

    @property
    def column(self):
        return self.__column

    @property
    def row(self):
        return self.__row

    def set_row(self, new_row):
        self.__row = new_row

    def set_column(self, new_column):
        self.__column = new_column



