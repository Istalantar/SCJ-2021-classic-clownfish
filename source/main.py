from typing import Union

import menus
from blessed import Terminal
from menus.utils import Menu


class Interface(Terminal):
    """Main program interface."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state: Menu = menus.StartMenu()

    def render(self) -> None:
        """Clear and render the screen depending on the current state."""
        print(self.clear + self.home + self.state.render(self))

    def kinput(self, code: Union[int, None]) -> None:
        """Propogate keyboard input."""
        if code == self.KEY_ENTER:
            self.state = self.state.click(self)
            self.selected = 0  # Reset
        else:
            self.selected = self.state.kinput(self, code)

    def main(self) -> None:
        """Start the main function taking care of the complete lifetime of the program."""
        while True:
            self.render()
            self.kinput(self.inkey().code)


if __name__ == '__main__':
    term = Interface()
    try:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            term.main()
    except KeyboardInterrupt:
        pass
