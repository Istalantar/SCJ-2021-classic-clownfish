from blessed import Terminal
from table import make_table


class Highscore:
    """Highscore Class"""

    filename = '../resources/highscore.csv'
    highscore = []  # List of Dictionary entries with following keys: 'Puzzle', 'Name', 'Time', 'Moves'

    def __init__(self):
        self.__read()

    def add(self, image: str, player_name: str, time: int, moves: int) -> None:
        """Adds new highscore to the list

        :param image: Name of the image for which to store the highscore
        :param player_name: Name of the player for whom to add a highscore
        :param time: Time (in seconds) used by the player so solve the puzzle
        :param moves: Moves needed by the player to solve the puzzle
        """
        new_entry = {'Puzzle': image, 'Name': player_name, 'Time': time, 'Moves': moves}
        self.highscore.append(new_entry)
        self.__save_entry()

    def display(self) -> None:
        """Display the player highscore"""
        term = Terminal()

        table = make_table(
            rows=[[entry['Puzzle'], entry['Name'], entry['Time'], entry['Moves']] for entry in self.highscore],
            labels=['Puzzle', 'Name', 'Time', 'Moves'])

        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.move_y(2))
            for line in table.split('\n'):
                print(term.center(line))
            term.inkey()

    def __save_entry(self) -> None:
        try:
            with open(self.filename, mode='a') as file:
                values = list(dict(self.highscore[-1]).values())
                values = [str(value) for value in values]
                file.write(','.join(values))
        except FileNotFoundError:
            pass  # TODO: error handling

    def __save(self) -> None:
        try:
            with open(self.filename, mode='w+') as file:
                file.write('highscore')  # TODO
        except FileNotFoundError:
            pass  # TODO: error handling

    def __read(self) -> None:
        try:
            with open(self.filename) as file:
                lines = file.readlines()
                for line in lines:
                    entry = line.strip().split(',')
                    self.highscore.append({'Puzzle': entry[0], 'Name': entry[1],
                                           'Time': entry[2], 'Moves': entry[3]})

        except FileNotFoundError:
            pass  # TODO: error handling


if __name__ == "__main__":
    test = Highscore()
    test.add('Blade', 'Dave', 999, 999)
