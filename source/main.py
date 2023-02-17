from source.service.game_service import GameService, Ai
from source.ui.console import Console
from source.ui.gui import Gui
from source.repository.board_repository import GameBoard
from source.domain.validators import PieceValidator


def run_game():
    piece_validator = PieceValidator()
    game_board = GameBoard(piece_validator)
    game_service = GameService(game_board, )
    ai = Ai(game_service, game_board)
    #console = Console(game_service, ai)
    #console.run_console()
    gui = Gui(game_service, ai)
    gui.run()


if __name__ == '__main__':
    run_game()

    # This is a Connect 4 game based on layered architecture programming
    # with GUI and console interface, the AI is build based on the mini-max
    # algorithm using the alpha-beta pruning optimisation