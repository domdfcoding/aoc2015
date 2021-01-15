"""
--- Day 11: Corporate Policy ---

Santa's previous password expired, and he needs help choosing a new one.

To help him remember his new password after the old one expires,
Santa has devised a method of coming up with a password based on the previous one.
Corporate policy dictates that passwords must be exactly eight lowercase letters (for security reasons),
so he finds his new password by incrementing his old password string repeatedly until it is valid.

Incrementing is just like counting with numbers: ``xx``, ``xy``, ``xz``, ``ya``, ``yb``, and so on.
Increase the rightmost letter one step;
if it was ``z``, it wraps around to ``a``, and repeat with the next letter to the left until one doesn't wrap around.

Unfortunately for Santa, a new Security-Elf recently started, and he has imposed some additional password requirements:

- Passwords must include one increasing straight of at least three letters, like ``abc``, ``bcd``, ``cde``, and so on, up to ``xyz``.
- They cannot skip letters; abd doesn't count.
- Passwords may not contain the letters ``i``, ``o``, or ``l``, as these letters can be mistaken for other characters and are therefore confusing.
- Passwords must contain at least two different, non-overlapping pairs of letters, like ``aa``, ``bb``, or ``zz``.

For example:

- ``hijklmmn`` meets the first requirement (because it contains the straight ``hij``) but fails the second requirement (because it contains `i` and `l`).
- ``abbceffg`` meets the third requirement (because it repeats ``bb`` and ``ff``) but fails the first requirement.
- ``abbcegjk`` fails the third requirement, because it only has one double letter (``bb``).
- The next password after ``abcdefgh`` is ``abcdffaa``.
- The next password after ``ghijklmn`` is ``ghjaabcc``,
  because you eventually skip all the passwords that start with ``ghi...``, since ``i`` is not allowed.

Given Santa's current password (your puzzle input), what should his next password be?
"""

# stdlib
from string import ascii_lowercase
# ==========================
from typing import Optional

print("Part One")
# ==========================

disallowed_letters = {l: ascii_lowercase.index(l) for l in "iol"}

# current_password = "abcdefgh"
# current_password = "ghijklmn"
current_password = "vzbxkghb"


def get_next_valid_password(password: str) -> Optional[str]:
	current_password = list(map(ascii_lowercase.index, password))

	cycle_count = 0

	while True:
		cycle_count += 1
		change_idx = -1

		while current_password[change_idx] == 25:
			change_idx -= 1

		new_password = current_password[:change_idx]
		new_password.append(current_password[change_idx] + 1)
		new_password.extend([0] * (abs(change_idx) - 1))

		current_password = new_password

		if any(char in current_password for char in disallowed_letters.values()):
			continue

		# Check for straight of three letters (increasing)
		straight = [current_password[0]]
		for char in current_password[1:]:
			if len(straight) == 3:
				break

			if char == straight[-1] + 1:
				straight.append(char)
			else:
				straight = [char]

		if len(straight) < 3:
			continue

		pairs = set()

		idx = 0
		while True:
			if idx >= (len(current_password) - 1):
				break

			char = current_password[idx]

			if char == current_password[idx + 1]:
				pairs.add((char, current_password[idx + 1]))
				idx += 1
			idx += 1

		if not pairs or len(pairs) < 2:
			continue

		return ''.join(map(ascii_lowercase.__getitem__, current_password))


first_valid_password = get_next_valid_password(current_password)

if first_valid_password is None:
	raise ValueError("No passwords are valid!")

print(
		"Santa's new password should be:", first_valid_password
		)  # vzbxxyzz  # lgtm [py/clear-text-logging-sensitive-data]

# ==========================
print("\nPart Two")
# ==========================
"""
Santa's password expired again. What's the next one?
"""

second_valid_password = get_next_valid_password(first_valid_password)

if second_valid_password is None:
	raise ValueError("No passwords are valid!")

print(
		"Santa's new password should be:", second_valid_password
		)  # vzcaabcc  # lgtm [py/clear-text-logging-sensitive-data]
