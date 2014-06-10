import unittest

from game_of_life import drawer
from game_of_life.board import Board


class DrawerTest(unittest.TestCase):

    def test_draw_board(self):
        board = Board(2, 2, live_cells=[(0, 1)])
        live_cell_character = 'X'
        dead_cell_character = 'O'
        results = drawer.Drawer(
            live_cell_character=live_cell_character,
            dead_cell_character=dead_cell_character
        ).draw(board)
        self.assertEqual(results, 'O O\nX O')


if __name__ == '__main__':
    unittest.main()
