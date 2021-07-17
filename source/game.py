import string
from os import path

from blessed import Terminal as Interface
from blessed.keyboard import Keystroke
from highscore import Highscore
from images import Image
from menus.utils import Menu
from sliding_puzzle import Puzzle


class Game(Menu):
    """Game menu where the user is playing."""

    def __init__(self, image: str):
        """Init function

        :param image: Image path
        :param difficulty: integer ranging from 1 to 5. Defaults to 1.
        """
        self.selected = 0
        self.player_name = ''

        self.path = image
        self.image = Image(image, 90)

        self.puzzle = Puzzle(self.image.generate_ascii, 2, 2)
        self.puzzle.shuffle()

    def render(self, term: Interface) -> str:
        """Render the game-menu."""
        # displayed content regardless of 'selected'
        rendered = term.move_y(3)  # just a spacing of four
        rendered += term.center(
            f'Moves: {self.puzzle.moves_done}' + term.move_right(4) + f'Time {self.puzzle.time_needed}'
        )
        rendered += term.move_down(1)

        for line in self.puzzle.draw(term).split('\n'):
            rendered += term.center(line)

        rendered += term.move_down(2)

        # selection on what to display below the puzzle
        if self.selected == 0:  # puzzle is active
            rendered += term.center('Use the arrow keys to move the pieces')
            rendered += term.center('Hit TAB to select "Exit"')
            rendered += term.move_xy(4, term.height - 3) + 'Exit'
        elif self.selected == 1:  # Exit button is selected
            rendered += term.center('Hit Enter to leave the puzzle')
            rendered += term.center('Hit TAB to go back to the puzzle')
            rendered += term.move_xy(4, term.height - 3) + term.black_on_white('Exit')
        elif self.selected == 2:  # puzzle is solved
            rendered += term.center(term.green_on_black('Congratulations, you completed the puzzle'))
            rendered += term.center('Please put in your name for the highscore (letters only): ' + self.player_name)

        return rendered

    def kinput(self, term: Interface, key: Keystroke) -> None:
        """Handle keyboard input (what button is selected)."""
        if self.selected == 0:  # input for puzzle mode
            if key.code == term.KEY_UP:
                self.puzzle.move_down()
            elif key.code == term.KEY_RIGHT:
                self.puzzle.move_left()
            elif key.code == term.KEY_DOWN:
                self.puzzle.move_up()
            elif key.code == term.KEY_LEFT:
                self.puzzle.move_right()
            elif key.code == term.KEY_TAB:
                self.selected = 1

            if self.puzzle.solved:  # Check if puzzle is solve, which also updates time elapsed
                # TODO: implement timeout for key input (time will only update, if key is hit)
                self.selected = 2
        elif self.selected == 1:  # input when 'Exit' is selected
            if key.code == term.KEY_TAB:
                self.selected = 0
        elif self.selected == 2:  # input when puzzle is solved
            if key in string.ascii_letters:
                self.player_name += key

            elif key.code in (term.KEY_BACKSPACE, term.KEY_DELETE):
                self.player_name = self.player_name[:-1]

    def click(self, term: Interface) -> Menu:
        """Handle a enter-press."""
        if self.selected == 1:
            from menus.start import StartMenu
            return StartMenu()
        elif self.selected == 2:
            Highscore().add(self.path, self.player_name, self.puzzle.moves_done, self.puzzle.time_needed)
            from menus.highscore_menu import HighScoreMenu  # Circular imports
            return HighScoreMenu()
        else:
            return self
