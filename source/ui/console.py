import math
import random

from tabulate import tabulate

from source.exceptions.exceptions import InvalidInput, InvalidColumn

from constants.constants import USER_TURN, COMPUTER_TURN, COMPUTER_PIECE, COLUMN_INDEX


class Console:

    def __init__(self, game_service, ai):
        self.__game_service = game_service
        self.__ai = ai

    def run_console(self):
        number_to_color = {
            '1': '🔴',
            "2": '🟠',
            "3": '🟢',
            '4': '🔵',
            '5': '🟣'
        }
        print("Welcome to Connect Four")
        while True:
            try:
                level_difficulty = int(input("Level of difficulty(1,2 or 3): "))
                if level_difficulty not in [1, 2, 3]:
                    raise InvalidInput("Invalid level selection")
            except InvalidInput as error:
                print(error)
            else:
                break
        while True:
            try:
                user_piece = input("""Select a color:
1 - 🔴
2 - 🟠
3 - 🟢
4 - 🔵
5 - 🟣
""")
                if user_piece not in ['1', '2', '3', '4', '5']:
                    raise InvalidInput("Invalid color selection")
                user_piece = number_to_color[user_piece]
            except InvalidInput as error:
                print(error)
            else:
                break
        turn = random.choice([USER_TURN, COMPUTER_TURN])
        while True:
            print(tabulate(self.__game_service.get_board(), headers=[' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 '],
                           tablefmt='grid'))
            print()
            winner = self.__game_service.is_winning_move()
            if winner is not None:
                if winner == 'draw':
                    print('Draw...')
                elif winner == user_piece:
                    print("User won!")
                else:
                    print("Computer won!")
                break
            turn %= 2
            if turn == USER_TURN:
                while True:
                    try:
                        try:
                            piece_column = int(input("Your turn, choose a column: "))
                        except ValueError:
                            raise InvalidInput("Column must be a number")
                        self.__game_service.drop_piece(piece_column - 1, user_piece)
                    except (InvalidInput, InvalidColumn) as error:
                        print(error)
                    else:
                        break
            else:
                print("AI is making a move...")
                piece_column = self.__ai.get_best_move(level_difficulty * 2,
                                                       -math.inf, math.inf, True, user_piece)[COLUMN_INDEX]
                self.__game_service.drop_piece(piece_column, COMPUTER_PIECE)
            turn += 1
