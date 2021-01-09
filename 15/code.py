"""
--- Day 15: Science for Hungry People ---

Today, you set out on the task of perfecting your milk-dunking cookie recipe.
All you have to do is find the right balance of ingredients.

Your recipe leaves room for exactly 100 teaspoons of ingredients.
You make a list of the remaining ingredients you could use to finish the recipe
(your puzzle input) and their properties per teaspoon:

- capacity (how well it helps the cookie absorb milk)
- durability (how well it keeps the cookie intact when full of milk)
- flavor (how tasty it makes the cookie)
- texture (how it improves the feel of the cookie)
- calories (how many calories it adds to the cookie)

You can only measure ingredients in whole-teaspoon amounts accurately,
and you have to be accurate so you can reproduce your results in the future.
The total score of a cookie can be found by adding up each of the properties
(negative totals become 0) and then multiplying together everything except calories.

For instance, suppose you have these two ingredients::

	Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
	Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

Then, choosing to use ``44`` teaspoons of butterscotch
and ``56`` teaspoons of cinnamon (because the amounts of each ingredient must add up to ``100``)
would result in a cookie with the following properties:

- A capacity of ``44*-1 + 56*2 = 68``
- A durability of ``44*-2 + 56*3 = 80``
- A flavor of ``44*6 + 56*-2 = 152``
- A texture of ``44*3 + 56*-1 = 76``

Multiplying these together (``68 * 80 * 152 * 76``, ignoring calories for now)
results in a total score of ``62842880``,
which happens to be the best score possible given these ingredients.
If any properties had produced a negative total,
it would have instead become zero,
causing the whole score to multiply to zero.

Given the ingredients in your kitchen and their properties,
what is the total score of the highest-scoring cookie you can make?
"""

# stdlib
import math
from typing import Optional

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

ingredients = {}

for line in [x for x in PathPlus("input.txt").read_lines() if x]:
	name, raw_properties = line.split(':')
	raw_properties = raw_properties.strip()
	ingredients[name] = dict(map(lambda x: (x[0], int(x[1])), map(str.split, raw_properties.split(", "))))


def find_best(max_calories: Optional[int] = None) -> int:
	all_totals = []

	for sprinkles in range(101):
		for butterscotch in range(101 - sprinkles):
			for chocolate in range(101 - butterscotch - sprinkles):
				for candy in range(101 - chocolate - butterscotch - sprinkles):
					if sum((sprinkles, butterscotch, chocolate, candy)) == 100:
						# print(sprinkles, butterscotch, chocolate, candy)

						totals = {
								"capacity": 0,
								"durability": 0,
								"flavor": 0,
								"texture": 0,
								"calories": 0,
								}

						for prop in totals:
							totals[prop] += ingredients["Sprinkles"][prop] * sprinkles
							totals[prop] += ingredients["Butterscotch"][prop] * butterscotch
							totals[prop] += ingredients["Chocolate"][prop] * chocolate
							totals[prop] += ingredients["Candy"][prop] * candy

						if max_calories is not None and totals["calories"] != max_calories:
							continue
						else:
							totals.pop("calories")

						product = math.prod(max(0, t) for t in totals.values())

						# print(product)
						# print(totals)
						# input(">>>")

						all_totals.append(product)

	return max(all_totals)


print("The highest scoring cookie possible has a score of:", find_best())  # 21367368

# ==========================
print("\nPart Two")
# ==========================
"""
Your cookie recipe becomes wildly popular!
Someone asks if you can make another recipe that has exactly ``500`` calories per cookie
(so they can use it as a meal replacement).
Keep the rest of your award-winning process the same
(100 teaspoons, same ingredients, same scoring system).

For example, given the ingredients above,
if you had instead selected ``40`` teaspoons of butterscotch and ``60`` teaspoons of cinnamon
(which still adds to 100), the total calorie count would be ``40*8 + 60*3 = 500``.
The total score would go down, though: only ``57600000``,
the best you can do in such trying circumstances.

Given the ingredients in your kitchen and their properties,
what is the total score of the highest-scoring cookie you can make with a calorie total of 500?
"""

print("The highest scoring cookie with 500 calories has a score of:", find_best(500))  # 1766400
