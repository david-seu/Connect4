import math
import sys
import random

import pygame

from constants.constants import BOARD_LENGTH, BOARD_WIDTH, BEIGE, BLACK, AQUA, \
    VIOLET, SQUARE_SIZE, RADIUS, LENGTH, SIZE, USER_TURN, COMPUTER_TURN, COLUMN_INDEX, FORMAT_LABEL,\
    MOUSE_POINTER_POSITION


class Gui:

    def __init__(self, game_service, ai):
        self.__game_service = game_service
        self.__ai = ai
        self.__screen = pygame.display.set_mode(SIZE)

    def __draw_board(self):
        for row in range(BOARD_WIDTH):
            for column in range(BOARD_LENGTH):
                pygame.draw.rect(self.__screen, BEIGE, (column * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE,
                                                        SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(self.__screen, BLACK,
                                   (int(column * SQUARE_SIZE + SQUARE_SIZE / 2),
                                    int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

        for row in range(BOARD_WIDTH):
            for column in range(BOARD_LENGTH):
                if self.__game_service.get_board()[row][column] == USER_TURN:
                    pygame.draw.circle(self.__screen, AQUA, (int(column * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                             int((row+1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
                elif self.__game_service.get_board()[row][column] == COMPUTER_TURN:
                    pygame.draw.circle(self.__screen, VIOLET, (int(column * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                               int((row+1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

    def __display_winner(self, game_over):
        gui_font = pygame.font.SysFont("monospace", 75)
        winner = self.__game_service.is_winning_move()
        if winner is not None:
            if winner == 'draw':
                label = gui_font.render("Draw...", True, BEIGE)
                self.__screen.blit(label, FORMAT_LABEL)
                game_over = True
            elif winner == USER_TURN:
                label = gui_font.render("Human wins!", True, AQUA)
                self.__screen.blit(label, FORMAT_LABEL)
                game_over = True
            else:
                label = gui_font.render("Computer wins!", True, VIOLET)
                self.__screen.blit(label, FORMAT_LABEL)

                game_over = True

            pygame.display.update()
        return game_over

    def run(self):
        pygame.init()
        game_over = False
        turn = random.choice([USER_TURN, COMPUTER_TURN % 2])

        self.__draw_board()
        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.__screen, BLACK, (0, 0, LENGTH, SQUARE_SIZE))
                    mouser_pointer_position = event.pos[MOUSE_POINTER_POSITION]
                    if turn == USER_TURN:
                        pygame.draw.circle(self.__screen, AQUA, (mouser_pointer_position, int(SQUARE_SIZE / 2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if turn == USER_TURN:
                        mouser_pointer_position = event.pos[MOUSE_POINTER_POSITION]
                        column = int(math.floor(mouser_pointer_position / SQUARE_SIZE))
                        if column in self.__game_service.get_available_columns():
                            pygame.draw.rect(self.__screen, BLACK, (0, 0, LENGTH, SQUARE_SIZE))
                            self.__game_service.drop_piece(column, USER_TURN)
                            turn += 1
                            turn = turn % 2
                            self.__draw_board()
                            game_over = self.__display_winner(game_over)
                        else:
                            print("Column full")

                else:
                    pass

            if turn + 2 == COMPUTER_TURN and not game_over:
                piece_column = self.__ai.get_best_move(6, -math.inf, math.inf, True, USER_TURN)[COLUMN_INDEX]
                self.__game_service.drop_piece(piece_column, COMPUTER_TURN)
                turn += 1
                turn = turn % 2
                self.__draw_board()
                game_over = self.__display_winner(game_over)

            if game_over:
                pygame.time.wait(5000)
