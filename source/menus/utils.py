import math
from typing import TYPE_CHECKING, Callable, Protocol

from blessed import Terminal as Interface
from blessed.keyboard import Keystroke

if TYPE_CHECKING:
    # Interface is a subclass of Terminal, importing it directly would cause circular imports
    from ..main import Interface  # noqa: F811


class Menu(Protocol):
    """Menu protocol that all menus implement."""

    def __init__(self) -> None:
        """Initialize the menu."""
        ...

    def render(self, term: Interface) -> str:
        """Render the menu, this method should return a string that will be printed."""
        ...

    def kinput(self, term: Interface, key: Keystroke) -> None:
        """Handle any keyboard input however the menu see fit.."""
        ...

    def click(self, term: Interface) -> 'Menu':  # Forward reference
        """Handle ENTER presses, this method should return a menu instance."""
        ...


class PopupMessage(Menu):
    """Popup message class"""

    def __init__(self, origin: Menu, message: str, color: Callable) -> None:
        """Initialize the popup message"""
        self.origin = origin
        self.message = message
        self.color = color

    def render(self, term: Interface) -> str:
        """Render the message waiting for the user to continue"""
        width = min(term.width - 8, len(self.message) + 12) - 2
        popup = [term.center('┌' + '—' * width + '┐')]
        popup.append(term.center('│' + ' ' * width + '│'))

        for item in (self.message, 'Press enter to continue'):
            popup.append(term.center(
                '│' + math.floor((width - len(item)) / 2) * ' '
                + self.color(item)
                + math.ceil((width - len(item)) / 2) * ' ' + '│'
            ))

            popup.append(term.center('│' + ' ' * width + '│'))

        popup.append(term.center('└' + '-' * width + '┘'))
        return term.move_y(term.height // 2) + '\n'.join(popup)

    def click(self, term: Interface) -> Menu:
        """Handle a enter-press."""
        return self.origin


def set_string_length(string: str, length: int) -> str:
    """Padd- or cut off - the string to make sure it is `length` long"""
    if len(string) == length:
        return string
    elif len(string) < length:
        return string + ' ' * (length - len(string))
    else:  # len(string) > length
        return string[:length - 3] + '...'
