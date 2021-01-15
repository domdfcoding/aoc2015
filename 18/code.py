"""
--- Day 18: Like a GIF For Your Yard ---

After the million lights incident, the fire code has gotten stricter:
now, at most ten thousand lights are allowed.
You arrange them in a 100x100 grid.

Never one to let you down, Santa again mails you instructions on the ideal lighting configuration.
With so few lights, he says, you'll have to resort to animation.

Start by setting your lights to the included initial configuration (your puzzle input).
A ``#`` means "on", and a ``.`` means "off".

Then, animate your grid in steps, where each step decides the next configuration based on the current one.
Each light's next state (either on or off) depends on its current state
and the current states of the eight lights adjacent to it (including diagonals).
Lights on the edge of the grid might have fewer than eight neighbors;
the missing ones always count as "off".

For example, in a simplified 6x6 grid, the light marked ``A`` has the neighbors numbered ``1`` through ``8``,
and the light marked ``B``, which is on an edge, only has the neighbors marked ``1`` through ``5``::

	1B5...
	234...
	......
	..123.
	..8A4.
	..765.

.
The state a light should have next is based on its current state (on or off)
plus the number of neighbors that are on:

- A light which is on stays on when ```2``` or ``3`` neighbors are on, and turns off otherwise.
- A light which is off turns on if exactly ``3`` neighbors are on, and stays off otherwise.

All of the lights update simultaneously;
they all consider the same current state before moving to the next.

Here's a few steps from an example configuration of another 6x6 grid::

	Initial state:
	.#.#.#
	...##.
	#....#
	..#...
	#.#..#
	####..

	After 1 step:
	..##..
	..##.#
	...##.
	......
	#.....
	#.##..

	After 2 steps:
	..###.
	......
	..###.
	......
	.#....
	.#....

	After 3 steps:
	...#..
	......
	...#..
	..##..
	......
	......

	After 4 steps:
	......
	......
	..##..
	..##..
	......
	......

After 4 steps, this example has four lights on.

In your grid of 100x100 lights, given your initial configuration, how many lights are on after 100 steps?.
"""

# stdlib
from collections import Counter
from itertools import chain
from typing import List

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

lights = [list(x) for x in PathPlus("input.txt").read_lines() if x]


def get_neighbours(x, y):
	coords = set()
	for xval in range(x - 1, x + 2):
		for yval in range(y - 1, y + 2):
			coords.add((min(max(0, xval), len(lights[0]) - 1), min(max(0, yval), len(lights) - 1)))

	coords.remove((x, y))

	return coords


def step(lights: List[List[str]]):

	new_lights = []

	for ypos, yval in enumerate(lights):
		new_lights.append([])
		for xpos, xval in enumerate(yval):
			on_neighbours = Counter(
					lights[neighbour[1]][neighbour[0]] for neighbour in get_neighbours(xpos, ypos)
					)['#']
			# print(xpos, ypos, xval, on_neighbours)

			if xval == '#' and on_neighbours in {2, 3}:
				new_lights[ypos].append('#')
			elif xval == '.' and on_neighbours == 3:
				new_lights[ypos].append('#')
			else:
				new_lights[ypos].append('.')

	return new_lights


# print("Initial state:")
# for line in lights:
# 	print("".join(line))

for n in range(100):
	# 	print(f"\nAfter {n+1} steps:")
	lights = step(lights)

	# for line in lights:
# 		print("".join(line))

n_lights_on = Counter(chain.from_iterable(lights))['#']
print(f"After 100 steps there are {n_lights_on} lights on.")  # 768

# ==========================
print("\nPart Two")
# ==========================
"""
You flip the instructions over; Santa goes on to point out that
this is all just an implementation of Conway's Game of Life.
At least, it was, until you notice that something's wrong
with the grid of lights you bought: four lights, one in each corner,
are stuck on and can't be turned off. The example above will actually run like this::

	Initial state:
	##.#.#
	...##.
	#....#
	..#...
	#.#..#
	####.#

	After 1 step:
	#.##.#
	####.#
	...##.
	......
	#...#.
	#.####

	After 2 steps:
	#..#.#
	#....#
	.#.##.
	...##.
	.#..##
	##.###

	After 3 steps:
	#...##
	####.#
	..##.#
	......
	##....
	####.#

	After 4 steps:
	#.####
	#....#
	...#..
	.##...
	#.....
	#.#..#

	After 5 steps:
	##.###
	.##..#
	.##...
	.##...
	#.#...
	##...#

After ``5`` steps, this example now has ``17`` lights on.

In your grid of 100x100 lights, given your initial configuration,
but with the four corners always in the on state, how many lights are on after 100 steps?
"""

lights = [list(x) for x in PathPlus("input.txt").read_lines() if x]

for n in range(100):
	lights = step(lights)
	lights[0][0] = '#'
	lights[0][-1] = '#'
	lights[-1][-1] = '#'
	lights[-1][0] = '#'

n_lights_on = Counter(chain.from_iterable(lights))['#']
print(f"After 100 steps with the broken lights there are {n_lights_on} lights on.")  # 781
