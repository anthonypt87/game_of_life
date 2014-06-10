import unittest

import mock

from game_of_life import errors
from game_of_life import loader
from game_of_life.board import Board


class LoaderTest(unittest.TestCase):

    def test_load_from_input(self):
        board = self._create_board_with_mock_input_function("0 0 0 0\n0 1 0 0")
        self.assertEqual(
            board,
            Board(4, 2, live_cells=[(1, 1)])
        )

    def _create_board_with_mock_input_function(self, input_return_value):
        board_loader = loader.Loader(
            input_function=mock.Mock(
                return_value=input_return_value
            )
        )
        return board_loader.load()

    def test_non_0_1_values_raises_invalid_board(self):
        self._check_invalid_input_raises_exception("0 0 0 0\n0 1 k 0")

    def _check_invalid_input_raises_exception(self, input_return_value):
        with self.assertRaises(errors.InvalidBoardError):
            self._create_board_with_mock_input_function(input_return_value)

    def test_inconsistent_length_raises_invalid_board(self):
        self._check_invalid_input_raises_exception("0 0\n0 1 k 0")

    def test_non_positive_length_raises_invalid_board(self):
        self._check_invalid_input_raises_exception("")

    def test_non_positive_x_length_raises_exception(self):
        self._check_invalid_input_raises_exception("\n1")


if __name__ == '__main__':
    unittest.main()
