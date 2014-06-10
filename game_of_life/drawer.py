# -*- coding: utf-8 -*-
class Drawer(object):
    """Responsible for drawing the board"""

    def __init__(self, live_cell_character='1', dead_cell_character='0'):
        self._live_cell_character = live_cell_character
        self._dead_cell_character = dead_cell_character

    def draw(self, board):
        """Draws and prints a `board`

        Args:
            board - `Board` object to print

        Example:
        Given the board, Board(2, 2, live_cells=[(1, 1)]), prints the
        following:
            '0 0\n0 1'
        """
        rows = []
        for y in xrange(board.y_size):
            row = ' '.join(
                self._draw_cell(board[x, y]) for x in xrange(board.x_size)
            )
            rows.append(row)

        return '\n'.join(rows)

    def _draw_cell(self, is_live_cell):
        if is_live_cell:
            return self._live_cell_character
        else:
            return self._dead_cell_character
