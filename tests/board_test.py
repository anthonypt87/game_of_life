import unittest

from game_of_life.board import Board
from game_of_life import errors


class BoardCreationTest(unittest.TestCase):

    def test_create_empty_board_and_check_location(self):
        board = Board(1, 1)
        self.assertEqual(board[0, 0], False)

    def test_board_with_valid_cell(self):
        board = Board(1, 2, live_cells=[(0, 1)])
        self.assertEqual(board[0, 1], True)

    def test_cant_create_live_cells_out_of_bounds(self):
        for invalid_cell in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            with self.assertRaises(errors.InvalidBoardError):
                Board(1, 1, live_cells=[invalid_cell])


class BoardStepTest(unittest.TestCase):

    def test_step_with_dead_cell_at_edge(self):
        board = self._create_board_and_step(1, 1)
        self.assertEqual(board[0, 0], False)

    def _create_board_and_step(self, *args, **kwargs):
        board = Board(*args, **kwargs)
        board.step()
        return board

    def test_step_with_live_cell_at_edge(self):
        board = self._create_board_and_step(1, 1, live_cells=[(0, 0)])
        self.assertEqual(board[0, 0], False)

    def test_three_live_cells_in_proximity_keep_you_alive(self):
        board = self._create_2_3_board_and_step(
            live_cells=[(0, 0), (0, 1), (0, 2)]
        )
        self.assertEqual(board[1, 1], True)

    def _create_2_3_board_and_step(self, live_cells):
        return self._create_board_and_step(2, 3, live_cells=live_cells)

    def test_four_cells_in_proximity_if_dead_leave_you_dead(self):
        board = self._create_2_3_board_and_step(
            live_cells=[(0, 0), (0, 1), (0, 2), (1, 0)]
        )
        self.assertEqual(board[1, 1], False)

    def test_four_cells_in_proximity_if_alive_keeps_you_alive(self):
        board = self._create_2_3_board_and_step(
            live_cells=[(0, 0), (0, 1), (0, 2), (1, 1)]
        )
        self.assertEqual(board[1, 1], True)

    def test_overpopulation_leads_to_death(self):
        board = self._create_2_3_board_and_step(
            live_cells=[(0, 0), (0, 1), (0, 2), (1, 2), (1, 1)]
        )
        self.assertEqual(board[1, 1], False)


class BoardEqualTest(unittest.TestCase):

    def test_equal(self):
        board_1 = Board(1, 1)
        board_2 = Board(1, 1, live_cells=[(0, 0)])
        board_3 = Board(1, 1)
        self.assertNotEqual(board_1, board_2)
        self.assertEqual(board_1, board_3)


if __name__ == '__main__':
    unittest.main()
