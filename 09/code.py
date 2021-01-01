"""
--- Day 9: All in a Single Night ---

Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit;
his elves have provided him the distances between every pair of locations.
He can start and end at any two (different) locations he wants, but he must visit each location exactly once.
What is the shortest distance he can travel to achieve this?

For example, given the following distances::

	London to Dublin = 464
	London to Belfast = 518
	Dublin to Belfast = 141

The possible routes are therefore::

	Dublin -> London -> Belfast = 982
	London -> Dublin -> Belfast = 605
	London -> Belfast -> Dublin = 659
	Dublin -> Belfast -> London = 659
	Belfast -> Dublin -> London = 605
	Belfast -> London -> Dublin = 982

The shortest of these is ``London -> Dublin -> Belfast = 605``, and so the answer is ``605`` in this example.

What is the distance of the shortest route?
"""

# stdlib
import re
from collections import defaultdict

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

# Parse the routes from the input
routes = defaultdict(dict)

for route in [x for x in PathPlus("input.txt").read_lines() if x]:
	m = re.match(r"([A-Za-z]+) to ([A-Za-z]+) = ([0-9]+)", route)

	routes[m.group(1)][m.group(2)] = int(m.group(3))
	routes[m.group(2)][m.group(1)] = int(m.group(3))

# iterate over the locations as the start points, and find the shortest route for each.
lengths = {}

for start_point in routes.keys():

	current_route = [start_point]
	current_location = current_route[-1]

	while True:
		# print(current_route)

		if len(current_route) == len(routes):
			break

		min_distance = 999999
		min_distance_dest = None

		for dest, distance in routes[current_location].items():
			if dest in current_route:
				continue

			if distance < min_distance:
				min_distance = distance
				min_distance_dest = dest

		# print(current_location, min_distance, min_distance_dest)
		current_location = min_distance_dest
		current_route.append(min_distance_dest)

	total_length = 0

	for idx, stop in enumerate(current_route[:-1]):
		# print(stop, routes[stop][current_route[idx + 1]])
		total_length += routes[stop][current_route[idx + 1]]

	# print(current_route[-1])
	# print(total_length)

	lengths[start_point] = total_length

print("The shortest overall length is:", min(lengths.values()))  # 251

# ==========================
print("\nPart Two")
# ==========================
"""
The next year, just to show off, Santa decides to take the route with the longest distance instead.

He can still start and end at any two (different) locations he wants,
and he still must visit each location exactly once.

For example, given the distances above,
the longest route would be ``982`` via (for example) ``Dublin -> London -> Belfast``.

What is the distance of the longest route?
"""

# iterate over the locations as the start points, and find the shortest route for each.
lengths = {}

for start_point in routes.keys():

	current_route = [start_point]
	current_location = current_route[-1]

	while True:
		# print(current_route)

		if len(current_route) == len(routes):
			break

		max_distance = -1
		max_distance_dest = None

		for dest, distance in routes[current_location].items():
			if dest in current_route:
				continue

			if distance > max_distance:
				max_distance = distance
				max_distance_dest = dest

		# print(current_location, max_distance, max_distance_dest)
		current_location = max_distance_dest
		current_route.append(max_distance_dest)

	total_length = 0

	for idx, stop in enumerate(current_route[:-1]):
		# print(stop, routes[stop][current_route[idx + 1]])
		total_length += routes[stop][current_route[idx + 1]]

	# print(current_route[-1])
	# print(total_length)

	lengths[start_point] = total_length

print("The longest overall length is:", max(lengths.values()))  # 898
