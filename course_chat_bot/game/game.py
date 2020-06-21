from course_chat_bot.game.Board import Board
from course_chat_bot.game.Renderer import Renderer
import random


class BossPuzzle:

    Board_size = 4

    def __init__(self):
        self.board = Board(BossPuzzle.Board_size)

    def get_board(self):
        return Renderer.render(self.board)

    def start_new_game(self):
        pos_number = random.randrange(1, len(self.board.Start_poses)-1)
        self.board.start_pose(pos_number)

    def action(self, command: str):
        coordinates = {}
        try:
            coordinates['first_x'] = ord(command.split()[0][0])-ord('a')+1
            coordinates['first_y'] = int(command.split()[0][1])
            coordinates['second_x'] = ord(command.split()[1][0])-ord('a')+1
            coordinates['second_y'] = int(command.split()[1][1])
            if not self.board.move_cells(coordinates):
                return False
            return True
        except BaseException:
            return False
