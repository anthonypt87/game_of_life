from game_of_life import errors
from game_of_life.board import Board


class Loader(object):
    """Loads and creates the Game of LIfe `Board` using the users input. A
    board should described as a string of 0's and 1's, 0's representing a dead
    cell, 1's representing a live cell. The cells should be delimited by spaces
    to represent seperate columns and newlines to represent seperate lows.

    Sample Valid Input:
    1 1 1 1 0
    0 1 1 0 0
    0 1 1 1 0
    """

    def __init__(self, input_function=None):
        """Creates the `BoardLoaderFromInput`

        Keyword Args:
            input_function - injected dependency to that takes in a users
                `input_function` and returns a string
        """
        self._input_function = input_function or parse_input

    def load(self):
        """Gets the raw string board using `self.input_function` and creates a
        `Board`."""
        lines = self._get_lines_from_input()

        if not lines:
            raise errors.InvalidBoardError

        x_length, y_length = self._get_board_dimension_from_lines(lines)

        live_cells = []
        for y, line in enumerate(lines):
            values = self._get_values(line)

            if len(values) != x_length:
                raise errors.InvalidBoardError

            for x, value in enumerate(values):
                if self._is_live_cell(value):
                    live_cells.append((x, y))

        return Board(x_length, y_length, live_cells=live_cells)

    def _get_lines_from_input(self):
        string_board = self._input_function()
        return string_board.splitlines()

    def _get_board_dimension_from_lines(self, lines):
        x_length = len(self._get_values(lines[0]))
        y_length = len(lines)
        return x_length, y_length

    def _get_values(self, line):
        return line.strip().split(' ')

    def _is_live_cell(self, value):
        if value == '1':
            return True
        elif value == '0':
            return False
        else:
            raise errors.InvalidBoardError

# Input Functions


def create_input_function_from_filename(input_filename):
    """Given an `input_filename` returns a function that reads and returns the
    data from from tne input file.

    Args:
        input_filename - filename of the input file to get data from
    """
    def load_from_file():
        with open(input_filename) as input_file:
            return input_file.read()
    return load_from_file


def parse_input():
    """Parses user input separated by new lines until an empty string is passed
    in.
    """
    return '\n'.join(iter(raw_input, ''))
