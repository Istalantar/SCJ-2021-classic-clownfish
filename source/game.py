
from typing import Union

from blessed import Terminal
from menus.utils import State
from sliding_puzzle import Puzzle


class Game:
    """Game class"""

    def __init__(self, image: str, difficulty: int = 1):
        """Init function

        :param image: image path
        :param difficulty: integer ranging from 1 to 5. Defaults to 1.
        """
        self.state = State.game

        difficulty = min(5, max(difficulty, 1))

        with open(image, 'r') as f:
            self.ascii = f.read()

        # Need to adjust the dimensions for sliding_puzzle.Puzzle
        vertical = 0
        horizontal = 0
        self.puzzle = Puzzle(self.ascii, vertical, horizontal)

    def render(self, term: Terminal, selected: int) -> str:
        """Render the start-menu."""
        rendered = term.move_y(3)  # just some spacing from the top for now
        rendered += self.puzzle.draw()

        return rendered

    def kinput(self, term: Terminal, selected: int, key: Union[int, None]) -> int:
        """Handle keyboard input (what button is selected)."""
        if key == term.KEY_UP:
            self.puzzle.move_up()
        elif key == term.KEY_RIGHT:
            self.puzzle.move_right()
        elif key == term.KEY_DOWN:
            self.puzzle.move_down()
        elif key == term.KEY_LEFT:
            self.puzzle.move_left()
        elif key == term.KEY_TAB:
            selected = 1

        return selected

    def click(self, term: Terminal, selected: int) -> State:
        """Handle a enter-press."""
        if selected == 1:
            return State.start
        else:
            return self.state
