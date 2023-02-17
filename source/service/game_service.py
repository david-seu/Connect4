import math
import random

from source.domain.entities import Piece
from constants.constants import EMPTY, PLAYER_ID, BOARD_LENGTH, BOARD_WIDTH, LAST_LOCATION, \
    CENTER_COLUMN_INDEX, FULL_BOARD, SCORE, COMPUTER_PIECE, END
from source.exceptions.exceptions import InvalidColumn


class GameService:

    def __init__(self, game_board):
        self.__game_board = game_board

    def __get_next_valid_row(self, piece):
        column = self.__game_board.get_column(piece.column)
        for index in reversed(range(len(column))):
            if column[index] == EMPTY:
                return index

    def get_available_columns(self):
        available_columns = []
        for column_index in range(BOARD_LENGTH):
            if self.__game_board.get_column(column_index)[LAST_LOCATION] == EMPTY:
                available_columns.append(column_index)
        return available_columns

    @staticmethod
    def __check_connect_4(connect_4_block):
        if connect_4_block.count(EMPTY) == 0 and connect_4_block.count(connect_4_block[PLAYER_ID]) == 4:
            return connect_4_block[PLAYER_ID]
        return None

    def get_board(self):
        return self.__game_board.board

    def drop_piece(self, piece_column, player_id):
        if piece_column not in self.get_available_columns():
            raise InvalidColumn("Column is full")
        piece = Piece(player_id, piece_column)
        piece.set_column(piece_column)
        piece.set_row(self.__get_next_valid_row(piece))
        self.__game_board.place_piece(piece)
        return piece

    def get_board_cell(self, row_index, column_index):
        return self.__game_board.get_column(column_index)[row_index]

    def is_winning_move(self):
        for row_index in reversed(range(BOARD_WIDTH)):
            for column_index in reversed(range(BOARD_LENGTH-3)):
                connect_4_block = self.__game_board.get_row(row_index)[column_index:column_index+4]
                winner = self.__check_connect_4(connect_4_block)
                if winner is not None:
                    return winner

        for column_index in reversed(range(BOARD_LENGTH)):
            for row_index in reversed(range(BOARD_WIDTH-3)):
                connect_4_block = self.__game_board.get_column(column_index)[row_index:row_index+4]
                winner = self.__check_connect_4(connect_4_block)
                if winner is not None:
                    return winner

        for row_index in reversed(range(BOARD_WIDTH-3)):
            for column_index in reversed(range(BOARD_LENGTH-3)):
                connect_4_block = [self.__game_board.board[row_index + counter][column_index + counter]
                                   for counter in range(4)]
                winner = self.__check_connect_4(connect_4_block)
                if winner is not None:
                    return winner

        for row_index in reversed(range(BOARD_WIDTH-3)):
            for column_index in reversed(range(BOARD_LENGTH-3)):
                connect_4_block = [self.__game_board.board[row_index + 3 - counter][column_index + counter]
                                   for counter in range(4)]
                winner = self.__check_connect_4(connect_4_block)
                if winner is not None:
                    return winner
        if self.__game_board.number_of_pieces == FULL_BOARD:
            return 'draw'
        return None


class Ai:
    def __init__(self, game_service, game_board):
        self.__game_service = game_service
        self.__game_board = game_board

    @staticmethod
    def __score_connect_4_block(connect_4_block, player_id, opponent_id):
        score = 0
        if connect_4_block.count(player_id) == 4:
            score = 100
        if connect_4_block.count(player_id) == 3 and connect_4_block.count(EMPTY) == 1:
            score = 6
        elif connect_4_block.count(player_id) == 2 and connect_4_block.count(EMPTY) == 2:
            score = 2

        if connect_4_block.count(opponent_id) == 3 and connect_4_block.count(EMPTY) == 1:
            score = -4
        return score

    def __score_board(self, player_id, opponent_id):
        score = 0
        center_column = self.__game_board.get_column(CENTER_COLUMN_INDEX)
        score += center_column.count(player_id) * 3

        for row_index in range(BOARD_WIDTH):
            for column_index in range(BOARD_LENGTH-3):
                connect_4_block = self.__game_board.get_row(row_index)[column_index:column_index+4]
                score += self.__score_connect_4_block(connect_4_block, player_id, opponent_id)

        for column_index in range(BOARD_LENGTH):
            for row_index in range(BOARD_WIDTH-3):
                connect_4_block = self.__game_board.get_column(column_index)[row_index:row_index+4]
                score += self.__score_connect_4_block(connect_4_block, player_id, opponent_id)

        for row_index in range(BOARD_WIDTH-3):
            for column_index in range(BOARD_LENGTH-3):
                connect_4_block = [self.__game_board.board[row_index + counter][column_index + counter]
                                   for counter in range(4)]
                score += self.__score_connect_4_block(connect_4_block, player_id, opponent_id)

        for row_index in range(BOARD_WIDTH-3):
            for column_index in range(BOARD_LENGTH-3):
                connect_4_block = [self.__game_board.board[row_index + 3 - counter][column_index + counter]
                                   for counter in range(4)]
                score += self.__score_connect_4_block(connect_4_block, player_id, opponent_id)

        return score

    def __is_terminal_node(self):
        if self.__game_service.is_winning_move() is not None:
            return True
        if self.__game_board.number_of_pieces == FULL_BOARD:
            return True
        return False

    def get_best_move(self, search_depth, ai_best_score, player_best_score, maximizing_player, user_piece):
        if search_depth == END or self.__is_terminal_node():
            if search_depth == END:
                if maximizing_player:
                    player_id = COMPUTER_PIECE
                    opponent_id = user_piece
                else:
                    player_id = user_piece
                    opponent_id = COMPUTER_PIECE
                return None, self.__score_board(player_id, opponent_id)
            else:
                if self.__game_service.is_winning_move() == COMPUTER_PIECE:
                    return None, 10000000
                elif self.__game_service.is_winning_move() == user_piece:
                    return None, -10000000
                else:
                    return None, 0
        if maximizing_player:
            optimal_score = - math.inf
            optimal_column = random.choice(self.__game_service.get_available_columns())
            for column in self.__game_service.get_available_columns():
                piece = self.__game_service.drop_piece(column, COMPUTER_PIECE)
                score = self.get_best_move(search_depth - 1, ai_best_score, player_best_score, False, user_piece)[SCORE]
                self.__game_board.remove_piece(piece)
                if score > optimal_score:
                    optimal_score = score
                    optimal_column = column
                ai_best_score = max(ai_best_score, optimal_score)
                if ai_best_score >= player_best_score:
                    break
            return optimal_column, optimal_score
        else:
            optimal_score = math.inf
            optimal_column = random.choice(self.__game_service.get_available_columns())
            for column in self.__game_service.get_available_columns():
                piece = self.__game_service.drop_piece(column, user_piece)
                score = self.get_best_move(search_depth - 1, ai_best_score, player_best_score, True, user_piece)[SCORE]
                self.__game_board.remove_piece(piece)
                if score < optimal_score:
                    optimal_score = score
                    optimal_column = column
                player_best_score = min(player_best_score, optimal_score)
                if ai_best_score >= player_best_score:
                    break
            return optimal_column, optimal_score
