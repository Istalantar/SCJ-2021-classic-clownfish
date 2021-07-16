
from typing import Union

from blessed import Terminal
from images import Image
from menus.utils import State, Menu
from sliding_puzzle import Puzzle


class Game(Menu):
    """Game menu where the user is playing."""

    def __init__(self, image: str, difficulty: int = 1):
        """Init function

        :param image: Image path
        :param difficulty: integer ranging from 1 to 5. Defaults to 1.
        """
        self.selected = 0

        difficulty = min(5, max(difficulty, 1))

        self.image = Image(image, 60)

        self.puzzle = Puzzle(self.image.generate_ascii, 2, 2)
        self.puzzle.shuffle()

    def render(self, term: Terminal) -> str:
        """Render the start-menu."""
        rendered = term.move_y(3)  # just some spacing from the top for now
        rendered += self.puzzle.draw()

        return rendered

    def kinput(self, term: Terminal, key: Union[int, None]) -> None:
        """Handle keyboard input (what button is selected)."""
        if key == term.KEY_UP:
            self.puzzle.move_down()
        elif key == term.KEY_RIGHT:
            self.puzzle.move_left()
        elif key == term.KEY_DOWN:
            self.puzzle.move_up()
        elif key == term.KEY_LEFT:
            self.puzzle.move_right()
        elif key == term.KEY_TAB:
            self.selected = int(not self.selected)

    def click(self, term: Terminal) -> State:
        """Handle a enter-press."""
        if self.selected == 1:
            return State.start
        else:
            return self.state
