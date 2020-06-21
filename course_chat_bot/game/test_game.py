import unittest
from unittest import mock
from course_chat_bot.game.Board import Board
from course_chat_bot.game.game import BossPuzzle
from course_chat_bot.game.Renderer import Renderer
import random


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board(4)
        self.board.start_pose(0)

    def tearDown(self):
        self.board = None

    def test_is_move_possible_1(self):
        coord_dict = {'first_x': self.board.size+1, 'first_y': self.board.size,
                      'second_x': self.board.size, 'second_y': self.board.size}
        self.assertEqual(self.board.is_move_possible(coord_dict), False)

    def test_is_move_possible_2(self):
        coord_dict = {'first_x': self.board.size-1,
                      'first_y': self.board.size-1,
                      'second_x': self.board.size,
                      'second_y': self.board.size}
        self.assertEqual(self.board.is_move_possible(coord_dict), False)

    def test_is_move_possible_3(self):
        coord_dict = {'first_x': self.board.size - 1,
                      'first_y': self.board.size - 1,
                      'second_x': self.board.size,
                      'second_y': self.board.size}
        self.assertEqual(self.board.is_move_possible(coord_dict), False)

    def test_is_move_possible_4(self):
        coord_dict = {'first_x': self.board.freecell[0],
                      'first_y': self.board.freecell[1],
                      'second_x': self.board.freecell[0]-1,
                      'second_y': self.board.freecell[1]}
        self.assertFalse(self.board.is_move_possible(coord_dict))

    def test_is_move_possible_5(self):
        coord_dict = {'first_x': self.board.freecell[0]-1,
                      'first_y': self.board.freecell[1],
                      'second_x': self.board.freecell[0],
                      'second_y': self.board.freecell[1]}
        self.assertTrue(self.board.is_move_possible(coord_dict))

    def test_start_pose(self):
        self.board.start_pose(1)
        self.assertEqual(self.board.numbs[1].x,
                         self.board.Start_poses[1][2][0])
        self.assertEqual(self.board.numbs[1].y,
                         self.board.Start_poses[1][2][1])

    def test_move_body(self):
        coord_dict = {'first_x': self.board.numbs[4].x,
                      'first_y': self.board.numbs[4].y,
                      'second_x': self.board.freecell[0],
                      'second_y': self.board.freecell[1]}
        self.board.move_body(coord_dict)
        self.assertEqual(self.board.numbs[4].x, coord_dict['second_x'])
        self.assertEqual(self.board.numbs[4].y, coord_dict['second_y'])

    def test_check_for_solving_1(self):
        self.board.start_pose(0)
        self.assertEqual(self.board.check_for_solving(), True)

    def test_check_for_solving_2(self):
        self.board.start_pose(1)
        self.assertEqual(self.board.check_for_solving(), False)

    def test_game_action(self):
        puzzle = BossPuzzle()
        puzzle.board.start_pose(0)
        self.assertEqual(puzzle.action('d3 d4'), True)

    def test_render_render_list(self):
        pos_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                    12, 13, 14, 15, 0]
        self.assertEqual(Renderer.render_list(self.board), pos_list)

    def test_render_render(self):
        msg = '● a  b  c  d  \n1 ①②③④\n' \
              '2 ⑤⑥⑦⑧\n3 ⑨⑩⑪⑫\n4 ⑬⑭⑮◯'
        self.assertEqual(Renderer.render(self.board), msg)

    def test_game_start_game(self):
        random.randrange = mock.MagicMock(return_value=0)
        puzzle = BossPuzzle()
        puzzle.start_new_game()
        self.assertEqual(puzzle.board.numbs[0].x, Board.Start_poses[0][1][1])


if __name__ == '__main__':
    unittest.main()
