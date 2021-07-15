import os
import sys
from typing import List

from blessed import Terminal
from game import Game
from highscore import Highscore

SUPPORTED_FILE_TYPES = ('.png', 'jpg')
INSIDE_THE_BOX = [
    r'┌────────────────────────────────────────────────────────────────────────────────────────┐',
    r'│                                                                                        │',
    r'│         ___ _   _ ____ ___ ____  _____    _____ _   _ _____    ____   _____  __        │',
    r'│        |_ _| \ | / ___|_ _|  _ \| ____|  |_   _| | | | ____|  | __ ) / _ \ \/ /        │',
    r'│         | ||  \| \___ \| || | | |  _|      | | | |_| |  _|    |  _ \| | | \  /         │',
    r'│         | || |\  |___) | || |_| | |___     | | |  _  | |___   | |_) | |_| /  \         │',
    r'│        |___|_| \_|____/___|____/|_____|    |_| |_| |_|_____|  |____/ \___/_/\_\        │',
    r'│                                                                                        │',
    r'│                                                                                        │',
    r'└────────────────────────────────────────────────────────────────────────────────────────┘',
]


def set_string_length(string: str, length: int) -> str:
    """Controll the length of any string by either padding with spaces,
    or cutting off string and ending with ...
    """
    if len(string) == length:
        return string
    elif len(string) < length:
        return string + ' ' * (length - len(string))
    else:  # len(string) > length
        return string[:length - 3] + '...'


def pad_number(num: int, length: int) -> str:
    """Pad any number with extra 0's at the start. e.g. 3 -> 003"""
    n = str(num)
    length = max(length, len(n))

    return n.rjust(length, '0')


def render_main(term: Terminal, index: int = 0) -> str:
    """Render main menu page"""
    rendered = ''

    splitted = [term.center(term.black_on_white(line) if index == 0 else line) for line in INSIDE_THE_BOX]
    rendered += '\n'.join(splitted) + '\n'

    rendered += term.move_y(term.height - 3)
    rendered += '    ' + term.black_on_white('Exit') if index == 1 else '    ' + 'Exit'
    return rendered


def render_table(term: Terminal, puzzles: List[dict], entries: int, index: int = 0) -> str:
    """Render highscore table

    :param term: blessed.Terminal object
    :param puzzles: List of puzzles and their highscores
    :param entries: Length of 'puzzles'
    :param index: Currently selected puzzle
    :return: Rendered table
    """
    rendered = ''

    rendered += (
        '    ' + set_string_length('Puzzle Name', term.width - 52)
        + '   ' + 'Player Name     '
        + '  ' + 'Highscore                  '
    ) + '\n\n'

    for i in range(entries):
        puzzle = puzzles[i]

        line = '    '
        line += set_string_length(puzzle['Puzzle'], term.width - 52) + '   '
        line += set_string_length(puzzle['Name'], 16) + '  '
        line += set_string_length(str(puzzle['Time']) + ' Seconds / ' + str(puzzle['Moves']) + ' Moves', 27)
        rendered += term.black_on_white(line) if index == i else line
        rendered += '\n'

    rendered += term.move_y(term.height - 3)
    rendered += '    ' + (term.black_on_white if index == entries else str)('Add new')
    return rendered


def render_file_explorer(term: Terminal, current_dir: str, files: List[str], dirs: List[str], index: int = 0) -> str:
    """Render file explorer

    Args:
        term (Terminal): blessed.Terminal object
        current_dir (str): currently selected directory
        files (List[str]): list of files
        dirs (List[str]): list of directories
        index (int, optional): index of selected file/dir in parent directory. Defaults to 0.

    Returns:
        str: [description]
    """
    rendered = ''
    rendered += term.black_on_white(set_string_length('    ' + current_dir, term.width)) + '\n\n'

    rendered += '\n'.join([
        (term.black_on_blue if index == i else term.blue)
        (set_string_length(dirs[i], term.width))
        for i in range(len(dirs))
    ]) + '\n'

    rendered += '\n'.join([
        (term.black_on_white if index - len(dirs) == i else str)
        (set_string_length(files[i], term.width))
        for i in range(len(files))
    ]) + '\n'

    return rendered


def select_new_puzzle(term: Terminal, current_dir: str = os.getcwd()) -> str:
    """Select image from local files

    Args:
        term (Terminal): blessed.Terminal objet
        current_dir (str, optional): directory currently selected. Defaults to os.getcwd().

    Returns:
        str: image path
    """
    print(term.clear + term.home)

    dirs = ['    ../']
    files = []

    for file in os.listdir(current_dir):
        if file.endswith(SUPPORTED_FILE_TYPES) and os.path.isfile(os.path.join(current_dir, file)):
            files.append('    ' + file)
        elif os.path.isdir(os.path.join(current_dir, file)):
            dirs.append('    ' + file + '/')

    index = 0
    while True:
        print(term.clear + term.home + render_file_explorer(term, current_dir, files, dirs, index))

        inp = term.inkey()
        if inp.code == term.KEY_UP:
            index -= 1
        elif inp.code == term.KEY_DOWN:
            index += 1
        elif inp.code == term.KEY_ENTER:
            break

        index = max(0, min(index, len(files) + len(dirs) - 1))

    if index < len(dirs):
        return select_new_puzzle(term, os.path.abspath(os.path.join(current_dir, dirs[index][4:])))

    return os.path.abspath(
        os.path.join(current_dir, files[index - len(dirs) - 1][4:])
    )


def main(term: Terminal) -> None:
    """Main function

    Args:
        term (Terminal): blessed.Terminal object
    """
    index = 0

    while True:
        print(term.clear + term.home + term.move_y(term.height // 2 - 3) + render_main(term, index))

        inp = term.inkey()
        if inp.code in (term.KEY_UP, term.KEY_DOWN):
            index = int(not index)
        elif inp.code == term.KEY_ENTER:
            if index == 0:
                break
            elif index == 1:
                sys.exit(0)

    index = 0
    puzzles = Highscore().highscore
    entries = len(puzzles)
    while True:
        print(term.clear + term.home + render_table(term, puzzles, entries, index))

        inp = term.inkey()
        if inp.code == term.KEY_UP:
            index -= 1
        elif inp.code == term.KEY_DOWN:
            index += 1
        elif inp.code == term.KEY_ENTER:
            if index != entries:
                break

            path = select_new_puzzle(term)
            Game(path)

        # Clamp index
        index = max(0, min(index, entries))

    output = term.clear + term.home
    '\n'.join(f'{key}: {puzzles[index][key]}' for key in puzzles[index])
    print(output)

    while True:
        pass


if __name__ == '__main__':
    term = Terminal()
    try:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            main(term)
    except KeyboardInterrupt:
        pass
