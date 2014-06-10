"""`Animators` are responsible for animating a board and their steps.

`Animators` need to implement an `animate()` function that take a `Board`
object that represents the initial game board state.
"""
import curses
import time


class PrintAllAnimator(object):
    """`Animator` that prints an iteration of the `Board` one step at a time,
    onto the screen, sleeping for a short time in between printing.
    """

    _sleep_time = 1

    def __init__(self, drawer):
        """Creates the `PrintAllAnimator`

        Args:
           drawer - `Drawer` object that describes how each board will be drawn
        """
        self._drawer = drawer

    def animate(self, board):
        """Given a `Board` representing the initial game state, draws the
        progression of the board over time, separating the steps of the board
        by new lines. This never stops running.

        Args:
            board - `Board` to animate
        """
        iteration = 1
        while True:
            to_print = 'Iteration %s\n' % iteration
            to_print += self._drawer.draw(board)
            to_print += '\n'
            print to_print
            iteration += 1
            board.step()
            time.sleep(self._sleep_time)


class CursesAnimator(object):
    """`Animator` that uses `curses`
    http://en.wikipedia.org/wiki/Curses_(programming_library), a terminal
    control library to animate the board.
    """

    def __init__(self, drawer):
        """Creates the `CursesAnimator`

        Args:
           drawer - `Drawer` object that describes how each board will be drawn
        """
        self._drawer = drawer

    def animate(self, board):
        """Animates the game board using curses to continually draw and refresh
        the screen. Finishes running when the user hits 'q'.
        """
        curses.wrapper(lambda _: self._run_curses(board))

    def _run_curses(self, board):
        screen = self._initialize_curses_screen()

        key_input = None
        iteration = 0

        # Continues to run until the user hits 'q'
        while key_input != ord('q'):
            self._draw_board_on_screen(screen, board, iteration)
            key_input = screen.getch()
            iteration += 1
            board.step()

        curses.endwin()

    def _initialize_curses_screen(self):
        screen = curses.initscr()
        screen.nodelay(1)
        screen.timeout(1000)
        return screen

    def _draw_board_on_screen(self, screen, board, iteration):
        screen.addstr(0, 0, 'Game Of Life')
        screen.addstr(
            1,
            0,
            'Welcome to the game of life! Hit q to quit or press or hold any'
        )
        screen.addstr(2, 0, 'other character to speed up the animation')

        screen.addstr(4, 0, 'Iteration %i' % iteration)
        screen.addstr(5, 0, self._drawer.draw(board))
        screen.refresh()


def print_function(string):
    """Used as an injected dependency because in Python 2.7, `print` is a
    statement and not a function."""
    print string


class SingleFrameAnimator(object):
    """Animates a single frame at a particular step"""

    def __init__(
        self,
        drawer,
        step_to_animate,
        print_function=print_function
    ):
        """Creates a `SingleFrameAnimator` object
        Args:
            drawer - `Drawer` object that describes how each board will be
                drawn
            step_to_animate - the step that we want to animate
        Keyword Args:
            print_function - injected dependency that describes how the output
                will be printed
        """
        self._drawer = drawer
        self._step_to_animate = step_to_animate
        self._print_function = print_function

    def animate(self, board):
        """Animates a single frame on the board described by
        `step_to_animate`
        """
        for _ in xrange(self._step_to_animate - 1):
            board.step()

        drawn_board = self._drawer.draw(board)
        self._print_function(drawn_board)
