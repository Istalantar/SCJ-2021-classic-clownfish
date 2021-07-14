from typing import List
import random
from dataclasses import dataclass


def walk(string: str, step: int) -> str:
    """Helper generator to iterate over a string with steps"""
    for i in range(0, len(string), step):
        yield string[i:i+step]


@dataclass
class PiecePosition:
    """A piece coordinates"""

    x: int
    y: int
    index: int


class PuzzlePiece:
    """Piece of a bigger puzzle."""

    index: int

    width: int
    height: int

    __slots__ = ('index', 'width', 'height', '_data')

    def __init__(self, index: int, width: int, height: int) -> None:
        self.index = index

        self.width = width
        self.height = height

        self._data = []

    def __repr__(self) -> str:
        return f'<PuzzlePiece index={self.index} width={self.width} height={self.height} empty={self.is_empty}>'

    def __str__(self) -> str:
        return '\n'.join(self.data)

    def __bool__(self) -> bool:
        return bool(self._data)

    @property
    def data(self) -> List[str]:
        """List of lines of the image."""
        return self._data or [" " * self.width] * self.height

    @property
    def is_empty(self) -> bool:
        """Whether this piece is empty (not filled)."""
        return bool(self)

    def append(self, string: str) -> None:
        """Append a string to the end of the data list."""
        self._data.append(string)

    def clear(self):
        self._data = list()


class Puzzle:
    """Main puzzle game class, taking care of the whole game logic."""

    rows: List[List[PuzzlePiece]]

    __slots__ = ('rows',)

    def __init__(self, image: str, horizontal: int, vertical: int) -> None:
        """Initialize the Puzzle with an image and size to split it by.

        :param image: An ASCII string that will be split
        :param horizontal: Amount of horizontal rows
        :param vertical: Amount of vertical rows
        """
        data = image.split('\n')

        length = len(data[0])
        for line in data:
            if length != len(line):  # Make sure that all strings are equal in length
                raise ValueError('Image is not a complete rectangle, make sure it is correctly padded.')

        # How many characters one piece is
        width = len(data[0]) / horizontal
        height = len(data) / vertical

        # We cannot handle decimals
        if not width.is_integer():
            raise ValueError(f'Image cannot be evenly split by width: {len(data[0])} / {horizontal}')
        elif not height.is_integer():
            raise ValueError(f'Image cannot be evenly split by height: {len(data)} / {vertical}')

        # Even though width and height have no decimals, they are still floats
        width, height = int(width), int(height)

        rows: List[List[PuzzlePiece]] = [
            [
                # This will give each PuzzlePiece an index from 0 to (horizontal*vertical - 1)
                PuzzlePiece(i, width, height) for i in range(v*horizontal, v*horizontal+horizontal)
            ] for v in range(vertical)
        ]

        for i, line in enumerate(data):
            for j, column in enumerate(walk(line, width)):
                rows[i//height][j].append(column)

        self.rows = rows

    def __repr__(self) -> str:
        return f'<Puzzle solved={self.solved} rows={self.rows}>'

    @property
    def solved(self) -> bool:
        """Whether the puzzle is considered solved."""
        i = 0
        for row in self.rows:
            for piece in row:
                if piece.index != i:
                    return False

                i += 1
        return True

    def _join(self, row: List[PuzzlePiece]) -> List[str]:
        """Join together a row of puzzle rows into a complete list of lines."""
        res = []
        for i in range(len(row[0].data)):
            res.append('')
            for piece in row:
                res[i] += piece.data[i]

        return res

    def draw(self) -> str:
        """Draw the puzzle in its current state."""
        output = []
        for row in self.rows:
            output.extend(self._join(row))

        return '\n'.join(output)

    def shuffle(self):
        for row in self.rows:
            random.shuffle(row)
        puzzle_heigth, puzzle_width = len(self.rows), len(self.rows[0])
        # empty one of the rows
        x = random.choice(range(puzzle_heigth))
        y = random.choice(range(puzzle_width))
        self.rows[x][y].clear()

    def _get_empty_piece_position(self) -> PiecePosition:
        x, y, index = [
            (x, y, piece.index)
            for x, row in enumerate(self.rows)
            for y, piece in enumerate(row)
            if piece._data == []
        ][0]
        return PiecePosition(x=x, y=y, index=index)

    def move_down(
        self,
    ):
        empty_pos = self._get_empty_piece_position()
        # return if empty piece is on the first row
        top_row = self.rows[0]
        if empty_pos.index in [piece.index for piece in top_row]:
            return
        # swap the empty piece with the target piece
        self.rows[empty_pos.x][empty_pos.y], self.rows[empty_pos.x - 1][empty_pos.y] = (
            self.rows[empty_pos.x - 1][empty_pos.y],
            self.rows[empty_pos.x][empty_pos.y],
        )

    def move_up(
        self,
    ):
        empty_pos = self._get_empty_piece_position()
        # return if empty piece is on the last row
        last_row = self.rows[-1]
        if empty_pos.index in [piece.index for piece in last_row]:
            return
        # swap the empty piece with the target piece
        self.rows[empty_pos.x][empty_pos.y], self.rows[empty_pos.x + 1][empty_pos.y] = (
            self.rows[empty_pos.x + 1][empty_pos.y],
            self.rows[empty_pos.x][empty_pos.y],
        )

    def move_right(
        self,
    ):
        empty_pos = self._get_empty_piece_position()
        # return if empty piece is on the last column
        puzzle_width = len(self.rows[0])
        last_column_y = puzzle_width - 1
        last_column = [piece for row in self.rows for j, piece in enumerate(row) if j == last_column_y]
        if empty_pos.index in [piece.index for piece in last_column]:
            return
        # swap the empty piece with the target piece
        self.rows[empty_pos.x][empty_pos.y], self.rows[empty_pos.x][empty_pos.y + 1] = (
            self.rows[empty_pos.x][empty_pos.y + 1],
            self.rows[empty_pos.x][empty_pos.y],
        )

    def move_left(
        self,
    ):
        empty_pos = self._get_empty_piece_position()
        # return if empty piece is on the first column
        first_column = [piece for row in self.rows for j, piece in enumerate(row) if j == 0]
        if empty_pos.index in [piece.index for piece in first_column]:
            return
        # swap the empty piece with the target piece
        self.rows[empty_pos.x][empty_pos.y], self.rows[empty_pos.x][empty_pos.y - 1] = (
            self.rows[empty_pos.x][empty_pos.y - 1],
            self.rows[empty_pos.x][empty_pos.y],
        )

