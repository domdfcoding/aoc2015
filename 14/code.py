"""
--- Day 14: Reindeer Olympics ---

This year is the Reindeer Olympics!
Reindeer can fly at high speeds, but must rest occasionally to recover their energy.
Santa would like to know which of his reindeer is fastest, and so he has them race.

Reindeer can only either be flying (always at their top speed) or resting (not moving at all),
and always spend whole seconds in either state.

For example, suppose you have the following Reindeer:

- Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
- Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

After one second, Comet has gone 14 km, while Dancer has gone 16 km.
After ten seconds, Comet has gone 140 km, while Dancer has gone 160 km.
On the eleventh second, Comet begins resting (staying at 140 km),
and Dancer continues on for a total distance of 176 km.
On the 12th second, both reindeer are resting.
They continue to rest until the 138th second, when Comet flies for another ten seconds.
On the 174th second, Dancer flies for another 11 seconds.

In this example, after the 1000th second, both reindeer are resting,
and Comet is in the lead at ``1120`` km (poor Dancer has only gotten ``1056`` km by that point).
So, in this situation, Comet would win (if the race ended at 1000 seconds).

Given the descriptions of each reindeer (in your puzzle input),
after exactly ``2503`` seconds, what distance has the winning reindeer traveled?
"""

# stdlib
import re
from collections import defaultdict
from operator import itemgetter
from typing import NamedTuple

# 3rd party
from domdf_python_tools.paths import PathPlus
from pandas import DataFrame

# ==========================
print("Part One")
# ==========================

specs = [x for x in PathPlus("input.txt").read_lines() if x]


class Reindeer(NamedTuple):
	name: str
	speed: int
	stamina: int
	rest: int

	@classmethod
	def from_string(cls, string):
		string = string.replace("but then must rest for ", '')

		m = re.match(r"^([A-Za-z]+) can fly ([0-9]+) km/s for ([0-9]+) seconds, ([0-9]+) seconds\.$", string)
		if m:
			return cls(m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)))

		raise ValueError("Invalid input.")


distances = {}

for entry in specs:
	reindeer = Reindeer.from_string(entry)

	distance = 0
	time = 0
	seconds_flying = 0

	while time < 2503:
		if seconds_flying == reindeer.stamina:
			seconds_flying = 0
			time += reindeer.rest
		else:
			distance += reindeer.speed
			time += 1
			seconds_flying += 1

	distances[reindeer.name] = distance

print(
		"The greatest distance travelled was {} by {}.".format(
				*reversed(max(distances.items(), key=itemgetter(1)))
				)
		)  # 2655

# ==========================
print("\nPart Two")
# ==========================
"""
Seeing how reindeer move in bursts, Santa decides he's not pleased with the old scoring system.

Instead, at the end of each second, he awards one point to the reindeer currently in the lead.
(If there are multiple reindeer tied for the lead, they each get one point.)
He keeps the traditional 2503 second time limit, of course, as doing otherwise would be entirely ridiculous.

Given the example reindeer from above, after the first second, Dancer is in the lead and gets one point.
He stays in the lead until several seconds into Comet's second burst: after the 140th second,
Comet pulls into the lead and gets his first point.
Of course, since Dancer had been in the lead for the 139 seconds before that, h
e has accumulated 139 points by the 140th second.

After the 1000th second, Dancer has accumulated ``689`` points,
while poor Comet, our old champion, only has ``312``.
So, with the new scoring system, Dancer would win (if the race ended at 1000 seconds).

Again given the descriptions of each reindeer (in your puzzle input),
after exactly ``2503`` seconds, how many points does the winning reindeer have?
"""

distances = DataFrame()

for entry in specs:
	reindeer = Reindeer.from_string(entry)

	distance = 0
	time = 0
	seconds_flying = 0
	distance_steps = []

	while time < 2503:
		if seconds_flying == reindeer.stamina:
			seconds_flying = 0
			time += reindeer.rest
			distance_steps.extend([distance] * reindeer.rest)

		else:
			distance += reindeer.speed
			time += 1
			seconds_flying += 1
			distance_steps.append(distance)

	distances[reindeer.name] = distance_steps[:2503]

scores = defaultdict(int)

for time, deer_distances in distances.iterrows():
	leader, max_distance = max(deer_distances.items(), key=itemgetter(1))

	for deer, distance in deer_distances.items():
		if distance == max_distance:
			scores[deer] += 1

print(
		"With the new scoring method, the reindeer with the highest score was {} with {}.".format(
				*max(scores.items(), key=itemgetter(1))
				)
		)  # 1059
