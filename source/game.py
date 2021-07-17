from typing import Union

from blessed import Terminal
from images import Image
from menus.utils import Menu, State
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

        self.image = Image(image, 90)

        self.puzzle = Puzzle(self.image.generate_ascii, 3, 3)
        self.puzzle.shuffle()

    def render(self, term: Terminal) -> str:
        """Render the game-menu."""
        rendered = term.move_y(3)  # just a spacing of four
        rendered += term.center(f'Moves: {self.puzzle.moves_done}' + term.move_right(4)
                                + f'Time {self.puzzle.time_needed}')

        rendered += term.move_down

        lines = self.puzzle.draw().split('\n')

        for line in lines:
            rendered += term.center(line)

        rendered += term.move_down(2)
        if self.selected != 3:  # image is not finished
            rendered += term.center('Use the arrow keys to move the pieces')
            rendered += term.center('Hit TAB + Enter to go back to the start menu')
        else:  # image is finished
            rendered += term.center(term.red_on_black('Congratulations, you completed the puzzle'))
        rendered += term.move_x(4) + (term.black_on_white('Exit') if self.selected == 1 else 'Exit')

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
        else:
            print('you hit an unsupported key')

        if self.puzzle.solved:  # Check if puzzle is solve, which also updates time elapsed
            # TODO: implement timeout for key input (time will only update, if key is hit)
            self.selected = 3

    def click(self, term: Terminal) -> State:
        """Handle a enter-press."""
        if self.selected == 1:
            return State.start
        else:
            return State.playing


if __name__ == '__main__':
    game = Game('../resources/phoenix.jpg')
    t_term = Terminal()
    print(game.render(t_term))
