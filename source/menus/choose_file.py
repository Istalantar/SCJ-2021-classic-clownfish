import os
from typing import TYPE_CHECKING

import PIL
from blessed import Terminal as Interface
from blessed.keyboard import Keystroke
from game import Game

from .utils import Menu, PopupMessage

if TYPE_CHECKING:
    # Interface is a subclass of Terminal, importing it directly would cause circular imports
    from ..main import Interface  # noqa: F811

SUPPORTED_FILE_TYPES = ('.png', '.jpg')


class ChooseFile(Menu):
    """Menu showing a file explorer for the user to navigate and pick a file."""

    def __init__(self) -> None:
        self.selected = 0

        self.init_files(os.getcwd())

    def init_files(self, folder: str) -> None:
        """List and save all files in the specified folder."""
        self.selected = 0  # Reset the selected item
        self.current_dir = folder

        self.dirs = ['../']  # Initialize with parent folder
        self.files = []
        for item in os.listdir(self.current_dir):
            if os.path.isdir(os.path.join(self.current_dir, item)):
                self.dirs.append(item + '/')

            else:
                self.files.append(item)

    def render(self, term: Interface) -> str:
        """Render the file explorer."""
        rendered = [
            # Make sure we don't go over the terminal width
            term.black_on_white(self.current_dir.ljust(term.width)[-term.width:]) + '\n'
        ]

        for i, item in enumerate(self.dirs):
            line = (' ' * 4 + item).ljust(term.width)

            rendered.append(term.black_on_blue(line) if self.selected == i else term.blue(line))

        for i, item in enumerate(self.files):
            line = (' ' * 4 + item).ljust(term.width)

            rendered.append(term.black_on_white(line) if self.selected == (i + len(self.dirs)) else line)

        return '\n'.join(rendered)

    def kinput(self, term: Interface, key: Keystroke) -> None:
        """Handle keyboard input for changing which button is selected."""
        if key.code == term.KEY_UP:
            self.selected -= 1
        elif key.code == term.KEY_DOWN:
            self.selected += 1

        self.selected = max(0, min(self.selected, len(self.dirs) + len(self.files) - 1))

    def click(self, term: Interface) -> Menu:
        """Handle a enter press, updating currently viewed files or changing state."""
        if self.selected < len(self.dirs):  # If it is a folder that is selected (they always come first)
            self.init_files(os.path.abspath(os.path.join(self.current_dir, self.dirs[self.selected])))
            return self  # Don't change state
          
        filename = self.files[self.selected - len(self.dirs)]
        try:
            return Game(
                os.path.abspath(
                    # The subtraction is to accomodate for directories being selected
                    os.path.join(self.current_dir, filename)
                )
            )
        except PIL.UnidentifiedImageError:
            # Invalid image
            return PopupMessage(self, f'Attempted to open {filename}, but did not recognize an image', term.red)
