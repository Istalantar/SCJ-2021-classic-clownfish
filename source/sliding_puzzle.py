from typing import List


class Puzzle:
    original_puzzle = None
    mixed_puzzle = None

    def __init__(self, puzzle: str):
        """

        :param puzzle: Puzzle as string
        """
        pass

    def randomize_puzzle(self, puzzle_size: int):
        """

        :param puzzle_size: Size of the puzzle -> x by x
        :return:
        """
        pass

    def move_up(self):
        pass

    def move_right(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def add_frame(self):
        """
        Adds the border around the single pieces of the puzzle
        :return:
        """
        pass

    def is_solved(self) -> bool:
        pass

    def print(self, puzzle):
        pass
