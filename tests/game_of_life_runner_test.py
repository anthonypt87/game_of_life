import unittest

import mock

import game_of_life_runner
from game_of_life import animators
from game_of_life.loader import Loader
from game_of_life.drawer import Drawer


class GameOfLifeRunnerIntegrationTest(unittest.TestCase):

    def test_whole_flow(self):
        print_function = mock.Mock()
        loader = Loader(
            input_function=lambda: '0 1 0\n0 1 0\n0 1 0'
        )
        drawer = Drawer()
        animator = animators.SingleFrameAnimator(
            drawer,
            2,
            print_function=print_function
        )

        runner = game_of_life_runner.GameOfLifeRunner(
            loader,
            animator
        )
        runner.run()

        print_function.assert_called_once_with('0 0 0\n1 1 1\n0 0 0')


if __name__ == '__main__':
    unittest.main()
