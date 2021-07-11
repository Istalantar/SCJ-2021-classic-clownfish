import os

from blessed import Terminal

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

amogus = '''           ,.....aa.,.
       ,J@p*""****qQ@k..
       j@´       ,__`¶@@,
      /@/   ,aQ@@@"""Q@@@,
      @@'  !@@G'       `"Qk,
 _.Jaa@µ   |@@@L          @k
!@µ´"]@|   `@@@@ka...aaaa@@@
|@|  @@|    Y@@@@@@@@@@@@@p`
/@|  @@|     "q"@@@@p""*¶@|
@@'  @@|                |@l
@@   @@|                |@@
@@   @@|                |@@
Q@;  @@|                |@|
!@l. @@|                @@`
 *Q@@@@\\     e@@kaaaao,@@
      @@     @@| ]@/'  |@|
      @@     @@| \\@;  /@!
      Q@a,_,J@@' `q@@@@pP
      `*q""""´'              '''

a, b, c = [], [], []
aa, ab, ac = [], [], []
ba, bb, bc = [], [], []
lines = amogus.split('\n')

win_width = len(lines[0])
win_height = len(lines)
img_width = len(lines[0])
img_height = len(amogus.split('\n'))

for line in lines[:win_height // 3]:
    a.append(line[:win_width // 3])
    b.append(line[win_width // 3:2 * (win_width // 3)])
    c.append(line[2 * (win_width // 3):])

for line in lines[win_height // 3:2 * (win_height // 3)]:
    aa.append(line[:win_width // 3])
    ab.append(line[win_width // 3:2 * (win_width // 3)])
    ac.append(line[2 * (win_width // 3):])

for line in lines[2 * (win_height // 3):]:
    ba.append(line[:win_width // 3])
    bb.append(line[win_width // 3:2 * (win_width // 3)])
    bc.append(line[2 * (win_width // 3):])

finish = []
one = []
for lines in zip(a, ba, ac):
    one.append(VERTICAL.join(['', lines[0], lines[1], lines[2], '']))
two = []
for lines in zip(b, ab, bc):
    two.append(VERTICAL.join(['', lines[0], lines[1], lines[2], '']))
three = []
for lines in zip(aa, bb, c):
    three.append(VERTICAL.join(['', lines[0], lines[1], lines[2], '']))

finish.extend([TOP_LEFT + HORIZONTAL * img_width + TOP_RIGHT])
finish.extend(one)
finish.extend([SEPERATOR_LEFT + HORIZONTAL * img_width + SEPERATOR_RIGHT])
finish.extend(two)
finish.extend([SEPERATOR_LEFT + HORIZONTAL * img_width + SEPERATOR_RIGHT])
finish.extend(three)
finish.extend([BOTTOM_LEFT + HORIZONTAL * img_width + BOTTOM_RIGHT])

os.system('cls' if os.name == 'nt' else 'clear')
term = Terminal()

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    print(term.move_y((term.height // 2) - (img_height // 2)))
    for line in finish:
        print(term.center(line))
    inp = term.inkey()
