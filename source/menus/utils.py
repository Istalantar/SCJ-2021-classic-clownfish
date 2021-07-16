from typing import TYPE_CHECKING, Callable, Protocol, Union

from blessed import Terminal as Interface

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

    def kinput(self, term: Interface, key: Union[int, None]) -> None:
        """Handle any keyboard input however the menu see fit."""
        ...

    def click(self, term: Interface) -> 'Menu':  # Forward reference
        """Handle ENTER presses, this method should return a menu instance."""
        ...


def set_string_length(string: str, length: int) -> str:
    """Padd- or cut off - the string to make sure it is `length` long"""
    if len(string) == length:
        return string
    elif len(string) < length:
        return string + ' ' * (length - len(string))
    else:  # len(string) > length
        return string[:length - 3] + '...'
