"""
--- Day 17: No Such Thing as Too Much ---

The elves bought too much eggnog again - ``150`` liters this time.
To fit it all into your refrigerator, you'll need to move it into smaller containers.
You take an inventory of the capacities of the available containers.

For example, suppose you have containers of size
``20``, ``15``, ``10``, ``5``, and ``5`` liters.
If you need to store ``25`` liters, there are four ways to do it:

- ``15`` and ``10``
- ``20`` and ``5`` (the first ``5``)
- ``20`` and ``5`` (the second ``5``)
- ``15``, ``5``, and ``5``

Filling all containers entirely,
how many different combinations of containers can exactly fit all 150 liters of eggnog?
"""

# stdlib
import heapq
import itertools
from collections import Counter
from operator import itemgetter

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

# containers = dict(enumerate([20, 15, 10, 5, 5]))
containers = dict(enumerate([int(x) for x in PathPlus("input.txt").read_lines() if x]))

total_eggnog = 150
# total_eggnog = 25

valid_perms = set()

for size in range(2, len(containers) + 1):
	for perm in itertools.combinations(containers.keys(), size):
		perm_containers = sorted(map(containers.__getitem__, perm))
		if sum(perm_containers) == total_eggnog:
			# print(perm_containers)
			valid_perms.add(tuple(sorted(perm)))

print(len(valid_perms))  # 654
print([sorted(map(containers.__getitem__, perm)) for perm in valid_perms])

# ==========================
print("\nPart Two")
# ==========================
"""
While playing with all the containers in the kitchen, another load of eggnog arrives!
The shipping and receiving department is requesting as many containers as you can spare.

Find the minimum number of containers that can exactly fit all ``150`` liters of eggnog.
How many different ways can you fill that number of containers
and still hold exactly ``150`` litres?

In the example above, the minimum number of containers was two.
There were three ways to use that many containers,
and so the answer there would be ``3``.
"""

frequencies = Counter(len(perm) for perm in valid_perms)
print(frequencies)

# print(heapq.nsmallest(1, frequencies.items(), key=itemgetter(1)))

print(frequencies[min(frequencies.keys())])  # 57
