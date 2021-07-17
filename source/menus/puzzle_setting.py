from blessed import Terminal as Interface
from blessed.keyboard import Keystroke
from game import Game
from menus.utils import Menu


class PuzzleSetting(Menu):
    """Menu to choose the settings for the puzzle"""

    def __init__(self, image: str):
        self.image = image
        self.selected = 0
        self.columns = 30
        self.rows = int(self.columns ** 0.43)
        self.horizontal = 2
        self.vertical = 2

    def render(self, term: Interface) -> str:
        """Renders the puzzle settings menu"""
        rendered = term.move_y(1)

        if self.selected in range(7):
            rendered += term.center('Pick the size the puzzle should have')
            rendered += self.__puzzle_size(term)
            # TODO: make it work
            # rendered += term.move_y(3)
            # rendered += term.center('┌' + '─' * (self.columns - 2) + '┐')
            # for _ in range(self.rows):
            #     rendered += term.center('│' + term.move_right(self.columns - 2) + '│')
            # rendered += term.center('└' + '─' * (self.columns - 2) + '┘')
        elif self.selected in range(10, 17, 1):
            rendered += term.center('Pick the number of puzzle pieces')
            rendered += self.__puzzle_pieces(term)
        else:
            rendered += term.center(f'Number of selected is: {self.selected}')

        return rendered

    def kinput(self, term: Interface, key: Keystroke) -> None:
        """Handles the inputs in the puzzle settings menu"""
        if key.code == term.KEY_LEFT:
            self.selected -= 1
        elif key.code == term.KEY_RIGHT:
            self.selected += 1

        if self.selected in range(7):  # settings for puzzle size
            if self.selected == 0:
                self.columns = 30
            elif self.selected == 1:
                self.columns = 40
            elif self.selected == 2:
                self.columns = 50
            elif self.selected == 3:
                self.columns = 60
            elif self.selected == 4:
                self.columns = 70
            elif self.selected == 5:
                self.columns = 80
            elif self.selected == 6:
                self.columns = 90
            self.rows = int(self.columns ** 0.43)
        elif self.selected in range(10, 17, 1):  # settings for number puzzle pieces
            if self.selected == 10:
                self.horizontal = 2
                self.vertical = 2
            elif self.selected == 11:
                self.horizontal = 3
                self.vertical = 2
            elif self.selected == 12:
                self.horizontal = 3
                self.vertical = 3
            elif self.selected == 13:
                self.horizontal = 4
                self.vertical = 3
            elif self.selected == 14:
                self.horizontal = 4
                self.vertical = 4
            elif self.selected == 15:
                self.horizontal = 5
                self.vertical = 4
            elif self.selected == 16:
                self.horizontal = 5
                self.vertical = 5
        elif self.selected < 0:
            self.selected = 0
        elif self.selected == 7:
            self.selected = 6
        elif self.selected == 9:
            self.selected = 10
        elif self.selected == 17:
            self.selected = 16

    def click(self, term: Interface) -> Menu:
        """Handles next action on Enter"""
        if self.selected in range(7):
            self.selected = 10
            return self
        elif self.selected >= 10:
            return Game(self.image, self.columns, self.horizontal, self.vertical)
        else:
            return self

    def __puzzle_size(self, term: Interface) -> str:
        rendered = ''

        if self.selected == 0:
            rendered += term.center(term.black_on_white(' 30 ') + ' 40 ' + ' 50 ' + ' 60 ' + ' 70 ' + ' 80 ' + ' 90 ')
        elif self.selected == 1:
            rendered += term.center(' 30 ' + term.black_on_white(' 40 ') + ' 50 ' + ' 60 ' + ' 70 ' + ' 80 ' + ' 90 ')
        elif self.selected == 2:
            rendered += term.center(' 30 ' + ' 40 ' + term.black_on_white(' 50 ') + ' 60 ' + ' 70 ' + ' 80 ' + ' 90 ')
        elif self.selected == 3:
            rendered += term.center(' 30 ' + ' 40 ' + ' 50 ' + term.black_on_white(' 60 ') + ' 70 ' + ' 80 ' + ' 90 ')
        elif self.selected == 4:
            rendered += term.center(' 30 ' + ' 40 ' + ' 50 ' + ' 60 ' + term.black_on_white(' 70 ') + ' 80 ' + ' 90 ')
        elif self.selected == 5:
            rendered += term.center(' 30 ' + ' 40 ' + ' 50 ' + ' 60 ' + ' 70 ' + term.black_on_white(' 80 ') + ' 90 ')
        elif self.selected == 6:
            rendered += term.center(' 30 ' + ' 40 ' + ' 50 ' + ' 60 ' + ' 70 ' + ' 80 ' + term.black_on_white(' 90 '))

        return rendered

    def __puzzle_pieces(self, term: Interface) -> str:
        rendered = ''

        if self.selected == 10:
            rendered += term.center(
                term.black_on_white(' 2x2 ') + ' 3x2 ' + ' 3x3 ' + ' 4x3 ' + ' 4x4 ' + ' 5x4 ' + ' 5x5 ')
        elif self.selected == 11:
            rendered += term.center(
                ' 2x2 ' + term.black_on_white(' 3x2 ') + ' 3x3 ' + ' 4x3 ' + ' 4x4 ' + ' 5x4 ' + ' 5x5 ')
        elif self.selected == 12:
            rendered += term.center(
                ' 2x2 ' + ' 3x2 ' + term.black_on_white(' 3x3 ') + ' 4x3 ' + ' 4x4 ' + ' 5x4 ' + ' 5x5 ')
        elif self.selected == 13:
            rendered += term.center(
                ' 2x2 ' + ' 3x2 ' + ' 3x3 ' + term.black_on_white(' 4x3 ') + ' 4x4 ' + ' 5x4 ' + ' 5x5 ')
        elif self.selected == 14:
            rendered += term.center(
                ' 2x2 ' + ' 3x2 ' + ' 3x3 ' + ' 4x3 ' + term.black_on_white(' 4x4 ') + ' 5x4 ' + ' 5x5 ')
        elif self.selected == 15:
            rendered += term.center(
                ' 2x2 ' + ' 3x2 ' + ' 3x3 ' + ' 4x3 ' + ' 4x4 ' + term.black_on_white(' 5x4 ') + ' 5x5 ')
        elif self.selected == 16:
            rendered += term.center(
                ' 2x2 ' + ' 3x2 ' + ' 3x3 ' + ' 4x3 ' + ' 4x4 ' + ' 5x4 ' + term.black_on_white(' 5x5 '))

        return rendered
