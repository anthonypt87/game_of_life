from game_of_life import errors


class Board(object):
    """Represents a Game of Life board.
    A board is described by it's dimensions, `x_size`, and `y_size`, and the
    live cells (`live_cells`) it contains. It knows how to progress itself to
    its next iteration through the `step()` function.
    """

    def __init__(self, x_size, y_size, live_cells=()):
        """Creates a new `Board` object.

        Args:
            x_size - integer describing the size of the x dimension
            y_size - integer describing the size of the y dimension

        Keyword Args:
            live_cells - iterable of (x, y) integer pairs representing live
                cells on the `Board` object.
        """
        self.x_size = x_size
        self.y_size = y_size
        self._live_cells = set(live_cells)
        self._ensure_live_cells_is_in_bounds()

    def _ensure_live_cells_is_in_bounds(self):
        for cell in self._live_cells:
            if not self._is_cell_in_bounds(cell):
                raise errors.InvalidBoardError

    def _is_cell_in_bounds(self, (x, y)):
        x_is_in_bounds = 0 <= x < self.x_size
        y_is_in_bounds = 0 <= y < self.y_size
        return x_is_in_bounds and y_is_in_bounds

    def __getitem__(self, cell):
        """Gets the current status of a particular cell, returning `True` if
        the cell is alive and `False` if it is not.

        Args:
            cell - (x, y) integer tuple representing the position to check

        Note: The way Python works with `__getitem__()` allows you to do
        board[1, 2], returning you the value at position (1, 2).
        """
        return cell in self._live_cells

    def __eq__(self, board):
        """Returns `True` if the boards are the same, where equality is defined
        by having the same dimensions and live cells.

        Args:
            board - the `Board` object to compare `self` to
        """
        return self.x_size == board.x_size and \
            self.y_size == board.y_size and \
            self._live_cells == board._live_cells

    def step(self):
        """Steps the game board according to the following rules (borrowed from
        Wikipedia):

        1. Any live cell with fewer than two live neighbours dies, as if caused
            by under-population.
        2. Any live cell with two or three live neighbours lives on to the next
            generation.
        3. Any live cell with more than three live neighbours dies, as if by
            overcrowding.
        4. Any dead cell with exactly three live neighbours becomes a live
            cell, as if by reproduction.

        Updates `self._live_cells` to represent the new set of live cells after
        the current iteration.
        """
        self._live_cells = set([
            cell for cell in self._get_cells_with_potential_updates()
            if self._should_cell_be_alive_in_next_step(cell)
        ])

    def _get_cells_with_potential_updates(self):
        cells_with_potential_updates = set([])
        for live_cell in self._live_cells:
            cells_in_proximity = self._get_cells_in_proximity(
                live_cell
            )
            cells_with_potential_updates.update(cells_in_proximity)
        return cells_with_potential_updates

    def _should_cell_be_alive_in_next_step(self, cell):
        cells_in_proximity = self._get_cells_in_proximity(cell)
        live_cells_in_proximity = self._live_cells & cells_in_proximity

        len_of_live_cells_in_proximity = len(live_cells_in_proximity)
        if len_of_live_cells_in_proximity == 3:
            return True
        elif len_of_live_cells_in_proximity == 4:
            return cell in self._live_cells
        else:
            return False

    def _get_cells_in_proximity(self, (x, y)):
        cells_in_proximity = set([])

        for x_candidate in xrange(x - 1, x + 2):
            for y_candidate in xrange(y - 1, y + 2):
                if self._is_cell_in_bounds((x_candidate, y_candidate)):
                    cells_in_proximity.add((x_candidate, y_candidate))

        return cells_in_proximity
