"""
--- Day 6: Probably a Fire Hazard ---

Because your neighbors keep defeating you in the holiday house decorating contest year after year,
you've decided to deploy one million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year,
Santa has mailed you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction;
the lights at each corner are at ``0,0``, ``0,999``, `999,999`, and ``999,0``.
The instructions include whether to turn on, turn off, or toggle various inclusive ranges given as coordinate pairs.
Each coordinate pair represents opposite corners of a rectangle, inclusive;
a coordinate pair like ``0,0 through 2,2`` therefore refers to 9 lights in a 3x3 square.
The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by doing the
instructions Santa sent you in order.

For example:

- ``turn on 0,0 through 999,999`` would turn on (or leave on) every light.
- ``toggle 0,0 through 999,0`` would toggle the first line of 1000 lights, turning off the ones that were on,
  and turning on the ones that were off.
- ``turn off 499,499 through 500,500`` would turn off (or leave off) the middle four lights.

After following the instructions, how many lights are lit?
"""

# stdlib
import re
from collections import Counter, defaultdict
from typing import Dict, Tuple

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

instructions = [x for x in PathPlus("input.txt").read_lines() if x]

lights: Dict[Tuple[int, int], bool] = defaultdict(bool)

for instruction in instructions:
	m = re.match(r"(turn on|turn off|toggle) ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)", instruction)

	assert m is not None

	for x_val in range(int(m.group(2)), int(m.group(4)) + 1):
		for y_val in range(int(m.group(3)), int(m.group(5)) + 1):

			if m.group(1) == "turn on":
				lights[(x_val, y_val)] = True

			elif m.group(1) == "turn off":
				lights[(x_val, y_val)] = False

			elif m.group(1) == "toggle":
				lights[(x_val, y_val)] = not lights[(x_val, y_val)]

count = Counter(lights.values())

assert sum(count.values()) <= 1000000

print(f"There are {count[True]} lights lit.")  # 569999

# ==========================
print("\nPart Two")
# ==========================
"""
You just finish implementing your winning light pattern when you realize you mistranslated Santa's message
from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls;
each light can have a brightness of zero or more.
The lights all start at zero.

The phrase ``turn on`` actually means that you should increase the brightness of those lights by ``1``.

The phrase ``turn off`` actually means that you should decrease the brightness of those lights by ``1``,
to a minimum of zero.

The phrase ``toggle`` actually means that you should increase the brightness of those lights by ``2``.

What is the total brightness of all lights combined after following Santa's instructions?

For example:

- ``turn on 0,0 through 0,0`` would increase the total brightness by ``1``.
- ``toggle 0,0 through 999,999`` would increase the total brightness by ``2000000``.
"""

dimmable_lights: Dict[Tuple[int, int], int] = defaultdict(int)

for instruction in instructions:
	m = re.match(r"(turn on|turn off|toggle) ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)", instruction)

	assert m is not None

	for x_val in range(int(m.group(2)), int(m.group(4)) + 1):
		for y_val in range(int(m.group(3)), int(m.group(5)) + 1):

			if m.group(1) == "turn on":
				dimmable_lights[(x_val, y_val)] += 1

			elif m.group(1) == "turn off":
				dimmable_lights[(x_val, y_val)] = max(dimmable_lights[(x_val, y_val)] - 1, 0)

			elif m.group(1) == "toggle":
				dimmable_lights[(x_val, y_val)] += 2

total_brightness = sum(dimmable_lights.values())

print(f"The total brightness is:", total_brightness)
