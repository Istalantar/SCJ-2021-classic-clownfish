from typing import TYPE_CHECKING

from blessed import Terminal as Interface
from blessed.keyboard import Keystroke
from game import Game
from highscore import Highscore

from .choose_file import ChooseFile
from .highscore_submenu import HighScoreSubMenu
from .utils import Menu, set_string_length

if TYPE_CHECKING:
    # Interface is a subclass of Terminal, importing it directly would cause circular imports
    from ..main import Interface  # noqa: F811


class HighScoreMenu(Menu):
    """The highscore menu."""

    def __init__(self):
        self.selected = 0

        self.highscores = Highscore().highscore
        self.puzzles = {}
        for hs in self.highscores:
            hs['Puzzle'] = hs['Puzzle'].split('/')[-1]
            if not hs['Puzzle'] in self.puzzles:
                self.puzzles[hs['Puzzle']] = hs
            else:
                puzzle = self.puzzles[hs['Puzzle']]
                if hs['Moves'] + hs['Time'] < puzzle['Moves'] + puzzle['Time']:
                    self.puzzles[hs['Puzzle']] = hs
                if hs['Moves'] + hs['Time'] == puzzle['Moves'] + puzzle['Time']:
                    self.puzzles[hs['Puzzle']] = {
                        'Puzzle': hs['Puzzle'],
                        'Name': 'Shared 1st place',
                        'Time': 0,
                        'Moves': 0
                    }

    def render(self, term: Interface) -> str:
        """Render the highscore table and a button to add new highscore."""
        rendered = []
        rendered.append(
            '    '
            + set_string_length('Puzzle name', term.width - 40)
            + set_string_length('Record holder', 32)
            + '    ' + '\n'
        )

        for i, puzzle in enumerate(self.puzzles):
            puzzle = self.puzzles[puzzle]
            rendered.append(
                (term.black_on_white if self.selected == i else str)(
                    '    '
                    + set_string_length(puzzle['Puzzle'], term.width - 40)
                    + set_string_length(puzzle['Name'], 32)
                    + '    '
                )
            )

        rendered.append(
            term.move_yx(term.height - 3, 4)
            + (term.black_on_white('From files') if self.selected == len(self.puzzles) else 'From files')
        )

        return '\n'.join(rendered)

    def click(self, term: Interface) -> Menu:
        """Handle enter key presses, changing state to file_explorer if the Add new button is selected."""
        if self.selected != len(self.puzzles):
            selected_puzzle_name: str
            for i, item in enumerate(self.puzzles):
                if i == self.selected:
                    selected_puzzle_name = item

            return HighScoreSubMenu(selected_puzzle_name)

        return ChooseFile()

    def kinput(self, term: Interface, key: Keystroke) -> None:
        """Handle arrow key input, changing the selected button."""
        if key.code == term.KEY_UP:
            self.selected -= 1
        elif key.code == term.KEY_DOWN:
            self.selected += 1

        # Clamp the value
        self.selected = max(0, min(self.selected, len(self.puzzles)))
