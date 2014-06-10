import argparse

from game_of_life import animators
from game_of_life.drawer import Drawer
from game_of_life.loader import Loader
from game_of_life.loader import create_input_function_from_filename
from game_of_life.loader import parse_input


class GameOfLifeRunner(object):
    """Responsible for loading an initial game board and animating it."""

    def __init__(self, loader, animator):
        """Creates a `GameOfLifeRunner` object.

        Args:
            loader - a `Loader` object that is used to load a game board
            animator - an `Animator` object used to animate the loaded board
        """
        self._loader = loader
        self._animator = animator

    def run(self):
        """Handles loading the board and animating it"""
        board = self._loader.load()
        self._animator.animate(board)


class RunnerCreatorFromArgs(object):
    """Handles the creation of a `GameOfLifeRunner` object.
    Given the results of `argparse.ArgumentParser.parse_args()`, an
    `argparse.Namespace` object, handles creationg `GameOfLifeRunner` objects.
    This object mainly handles wiring everything together given the input
    arguments.
    """

    def __init__(self, args):
        """Creates a `RunnerCreatorFromArgs` object

        Args:
            args - a `argparse.Namespace` object that describes the command
                line arguments of the script
        """
        self._args = args

    def create(self):
        """Creates a `GameOfLifeRunner` object using the command line
        arguments.
        """
        loader = self._create_loader()
        drawer = self._create_drawer()
        animator = self._create_animator(drawer)
        return GameOfLifeRunner(loader, animator)

    def _create_loader(self):
        if self._args.filename:
            input_function = create_input_function_from_filename(
                self._args.filename
            )
        else:
            input_function = parse_input

        return Loader(input_function)

    def _create_drawer(self):
        drawer_params = {
            'live_cell_character': self._args.output_live_cell_character,
            'dead_cell_character': self._args.output_dead_cell_character,
        }
        return Drawer(**drawer_params)

    def _create_animator(self, drawer):
        self._validate_animator_args()

        if self._args.step_to_print is not None:
            return animators.SingleFrameAnimator(
                drawer,
                self._args.step_to_print
            )

        animator_cls = self._animator_name_to_animator_cls_map.get(
            self._args.animator,
            animators.CursesAnimator
        )
        return animator_cls(drawer)

    def _validate_animator_args(self):
        has_step_to_print = bool(self._args.step_to_print)
        has_animator = bool(self._args.animator)

        has_no_options_set = not (has_step_to_print or has_animator)
        if has_no_options_set:
            return

        has_both_options_set = has_step_to_print and has_animator
        if has_both_options_set:
            raise argparse.ArgumentTypeError(
                'Cant have both --step-to-print and --animator options.'
            )

        has_invalid_animator_name = self._args.animator not in \
            self._animator_name_to_animator_cls_map
        if has_animator and has_invalid_animator_name:
            raise argparse.ArgumentTypeError(
                'Invalid --animator. Must be one of %s' %
                self._animator_name_to_animator_cls_map.keys()
            )

    _animator_name_to_animator_cls_map = {
        'curses': animators.CursesAnimator,
        'print_all': animators.PrintAllAnimator
    }


def parse_args():
    parser = argparse.ArgumentParser(
        usage=""" %(prog)s [options].

If "--filename" is not passed in, the user can type in the board they want to
test. Boards should look like:

0 0
0 1

where "0"s represent dead cells and "1"s represent live cells. Hit return twice
when done drawing the board.

By default uses `curses` to draw the output. If using a non unix like OS,
please use "--animator print_all" for a less pleasant but working experience.
Important caveat: a "_curses.error" will be raised if your screen resolution is
too small for larger boards.

Sample Calls:
python %(prog)s --filename=boards/gosper_glider_gun.txt
    --output-dead-cell-character=' ' <-- My favorite
python %(prog)s --filename=boards/h.txt --output-live-cell-character=' '
    --output-dead-cell-character='X' <-- Also really cool
python %(prog)s
python %(prog)s --filename=boards/blinker.txt --step-to-print=5
python %(prog)s --filename=boards/beacon.txt --animator=print_all
"""
    )
    parser.add_argument(
        '--animator',
        help="""How to animate the game of life. Acceptable ANIMATORS include:
        "curses", and "print_all". "curses" uses `curses`, a terminal control
        library for Unix-like systems to draw and refresh the screen.  Hitting
        "q" will quit out of the process. "print_all" prints each iteration,
        one at a time, blank line separated. "print_all" creates an animator
        that runs indefinitely so this process will need to be explicitly
        killed via ctrl-c. The default ANIMATOR is "curses". This can not be
        used together with "--step-to-print"""
    )
    parser.add_argument(
        '--filename',
        help="""If passed in takes a input file that describes the initial
        grid.  Grids look like "0", "1" with spaces representing different
        columns and new lines representing different rows. Please look at
        "boards/blinker.txt" to see an example of a valid board."""
    )
    parser.add_argument(
        '--step-to-print',
        type=int,
        help="""The step to print. The initial step is step 1. This can not be
        used together with "--animator".
        """
    )
    parser.add_argument(
        '--output-live-cell-character',
        help="""Character to represent a living cell during animation. Defaults
        to "1"
        """,
        default='1'
    )
    parser.add_argument(
        '--output-dead-cell-character',
        help="""Character to represent a living cell during animation. Defaults
        to "0"
        """,
        default='0'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    creator = RunnerCreatorFromArgs(args)
    runner = creator.create()
    runner.run()
