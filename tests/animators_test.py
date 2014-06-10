import unittest

import mock

from game_of_life import animators


class SingleFrameAnimatorTest(unittest.TestCase):

    def test_animate_prints_board_after_x_iterations(self):
        step_to_animate = 3
        drawer = mock.Mock()
        print_function = mock.Mock()
        animator = animators.SingleFrameAnimator(
            drawer,
            step_to_animate,
            print_function=print_function
        )

        board = mock.Mock()
        animator.animate(board)

        self.assertEqual(board.step.call_count, step_to_animate - 1)
        drawer.draw.assert_called_once_with(board)
        print_function.assert_called_once_with(drawer.draw.return_value)


if __name__ == '__main__':
    unittest.main()
