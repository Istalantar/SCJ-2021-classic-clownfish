from typing import List


def walk(string: str, step: int) -> str:
    """Helper generator to iterate over a string with steps"""
    for i in range(0, len(string), step):
        yield string[i:i+step]


class PuzzlePiece:
    """Piece of a bigger puzzle."""

    width: int
    height: int

    __slots__ = ('width', 'height', '_data')

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self._data = []

    def __repr__(self) -> str:
        return f'<PuzzlePiece width={self.width} height={self.height} empty={self.empty}>'

    def __str__(self) -> str:
        return '\n'.join(self.data)

    def __bool__(self) -> bool:
        return bool(self._data)

    @property
    def data(self) -> List[str]:
        """List of lines of the image."""
        return self._data or [' ' * self.width] * self.height

    @property
    def empty(self) -> bool:
        """Whether this piece is empty (not filled)."""
        return bool(self)

    def append(self, string: str) -> None:
        """Append a string to the end of the data list."""
        self._data.append(string)


class Puzzle:
    """Main puzzle game class, taking care of the whole game logic."""

    pieces: List[List[PuzzlePiece]]

    __slots__ = ('pieces',)

    def __init__(self, image: str, horizontal: int, vertical: int) -> None:
        """Initialize the Puzzle with an image and size to split it by.

        :param image: An ASCII string that will be split
        :param horizontal: Amount of horizontal pieces
        :param vertical: Amount of vertical pieces
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

        pieces: List[List[PuzzlePiece]] = [
            [PuzzlePiece(width, height) for _ in range(horizontal)] for _ in range(vertical)
        ]

        for i, line in enumerate(data):
            for j, column in enumerate(walk(line, width)):
                pieces[i//height][j//width].append(column)

        self.pieces = pieces

    def __repr__(self) -> str:
        return f'<Puzzle pieces={self.pieces}>'

    def _join(self, row: List[PuzzlePiece]) -> List[str]:
        """Join together a row of puzzle pieces into a complete list of lines."""
        res = []
        for i in range(len(row[0].data)):
            res.append('')
            for piece in row:
                res[i] += piece.data[i]

        return res

    def draw(self) -> str:
        """Draw the puzzle in its current state."""
        output = []
        for row in self.pieces:
            output.extend(self._join(row))

        return '\n'.join(output)
