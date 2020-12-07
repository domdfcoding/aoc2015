"""
--- Day 3: Perfectly Spherical Houses in a Vacuum ---

Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location,
and then an elf at the North Pole calls him via radio and tells him where to move next.
Moves are always exactly one house to the north (``^``), south (``v``), east (``>``), or west (``<``).
After each move, he delivers another present to the house at his new location.

However, the elf back at the north pole has had a little too much eggnog,
and so his directions are a little off, and Santa ends up visiting some houses more than once.
How many houses receive at least one present?

For example:

- ``>`` delivers presents to ``2`` houses: one at the starting location, and one to the east.
- ``^>v<`` delivers presents to ``4`` houses in a square, including twice to the house at his starting/ending location.
- ``^v^v^v^v^v`` delivers a bunch of presents to some very lucky children at only ``2`` houses.
"""

# stdlib
from typing import Iterable, Set, Tuple

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

directions = [x for x in list(PathPlus("input.txt").read_text()) if x]


def get_houses_visited(directions: Iterable[str]) -> Set[Tuple[int, int]]:
	x_pos, y_pos = 0, 0
	history = {(0, 0)}

	for direction in directions:
		if direction == '^':
			y_pos += 1
		elif direction == 'v':
			y_pos -= 1
		elif direction == '>':
			x_pos += 1
		elif direction == '<':
			x_pos -= 1

		if (x_pos, y_pos) not in history:
			history.add((x_pos, y_pos))

	return history


print(f"Santa delivers to {len(get_houses_visited(directions))} houses")  # 2592

# ==========================
print("\nPart Two")
# ==========================
"""
The next year, to speed up the process, Santa creates a robot version of himself,
Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the same starting house),
then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

- ``^v`` delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
- ``^>v<`` now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
- ``^v^v^v^v^v`` now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.
"""

santa_directions = directions[0::2]
robo_santa_directions = directions[1::2]

santa_deliveries = get_houses_visited(santa_directions)
robo_santa_deliveries = get_houses_visited(robo_santa_directions)

houses_visited = santa_deliveries | robo_santa_deliveries

print(f"Santa and Robot-Santa deliver to {len(houses_visited)} houses")  # 2360
