from typing import Any, List, Optional

VERTICAL = '│'
HORIZONTAL = '─'
TOP_LEFT = '┌'
TOP_SEPERATOR = '┬'
TOP_RIGHT = '┐'
SEPERATOR_LEFT = '├'
SEPERATOR_MIDDLE = '┼'
SEPERATOR_RIGHT = '┤'
BOTTOM_LEFT = '└'
BOTTOM_SEPERATOR = '┴'
BOTTOM_RIGHT = '┘'


def make_table(rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False) -> str:
    """Creates a table for the input data

    :param rows: 2D list containing objects that have a single-line representation (via `str`).
    All rows must be of the same length.
    :param labels: List containing the column labels. If present, the length must equal to that of each row.
    :param centered: If the items should be aligned to the center, else they are left aligned.
    :return: A table representing the rows passed in.
    """
    column_count = len(rows[0])

    temp_rows = rows.copy()
    if labels is not None:
        temp_rows.append(labels)
    column_width = get_column_size(column_count, temp_rows)

    table_string = make_top_border(column_width) + '\n'
    if labels is not None:
        table_string += make_row(column_count, column_width, centered, labels) + '\n'
        table_string += make_separator(column_width) + '\n'
    for row in rows:
        table_string += make_row(column_count, column_width, centered, row) + '\n'
    table_string += make_bottom_border(column_width)

    return table_string


def get_column_size(column_count: int, rows: List) -> List:
    """Gets column size

    :param column_count:
    :param rows:
    :return:
    """
    column_size = [0 for i in range(column_count)]

    for row in rows:
        for i in range(column_count):
            if len(str(row[i]).strip()) > column_size[i]:
                column_size[i] = len(str(row[i]).strip())

    return column_size


def make_top_border(column_width: List[int]) -> str:
    """Creates the string for the top border of the table

    :param column_width:
    :return:
    """
    my_string = f'{TOP_LEFT}'
    i_max = len(column_width)
    for i in range(len(column_width)):
        my_string += f'{(column_width[i] + 2) * HORIZONTAL}'
        if i < i_max - 1:
            my_string += f'{TOP_SEPERATOR}'
        else:
            my_string += f'{TOP_RIGHT}'
    return my_string


def make_bottom_border(column_width: List[int]) -> str:
    """Creates the string for the bottom border of the table

    :param column_width:
    :return:
    """
    my_string = f'{BOTTOM_LEFT}'
    i_max = len(column_width)
    for i in range(len(column_width)):
        my_string += f'{(column_width[i] + 2) * HORIZONTAL}'
        if i < i_max - 1:
            my_string += f'{BOTTOM_SEPERATOR}'
        else:
            my_string += f'{BOTTOM_RIGHT}'
    return my_string


def make_separator(column_width: List[int]) -> str:
    """Creates the string for the horizontal separator of the table

    :param column_width:
    :return:
    """
    my_string = f'{SEPERATOR_LEFT}'
    i_max = len(column_width)
    for i in range(len(column_width)):
        my_string += f'{(column_width[i] + 2) * HORIZONTAL}'
        if i < i_max - 1:
            my_string += f'{SEPERATOR_MIDDLE}'
        else:
            my_string += f'{SEPERATOR_RIGHT}'
    return my_string


def make_row(column_count: int, column_width: List, centered: bool, row: List) -> str:
    """Creates the string for one row of the table

    :param column_count:
    :param column_width:
    :param centered:
    :param row:
    :return:
    """
    my_string = VERTICAL

    if centered:
        for i in range(column_count):
            fill_count = column_width[i] - len(str(row[i]))
            left_fill = int(fill_count / 2)
            right_fill = fill_count - left_fill
            my_string += f" {left_fill * ' '}{row[i]}{right_fill * ' '} {VERTICAL}"
    else:
        for i in range(column_count):
            fill_count = column_width[i] - len(str(row[i]))
            my_string += f" {row[i]}{fill_count * ' '} {VERTICAL}"

    return my_string
