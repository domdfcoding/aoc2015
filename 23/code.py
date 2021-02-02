"""
--- Day 23: Opening the Turing Lock ---

Little Jane Marie just got her very first computer for Christmas from some unknown benefactor.
It comes with instructions and an example program, but the computer itself seems to be malfunctioning.
She's curious what the program does, and would like you to help her run it.

The manual explains that the computer supports two registers and six instructions
(truly, it goes on to remind the reader, a state-of-the-art technology).
The registers are named a and b, can hold any non-negative integer, and begin with a value of ``0``.
The instructions are as follows:

- ``hlf r`` sets register ``r`` to half its current value, then continues with the next instruction.
- ``tpl r`` sets register ``r`` to triple its current value, then continues with the next instruction.
- `inc r` increments register ``r``, adding ``1`` to it, then continues with the next instruction.
- ``jmp offset`` is a jump; it continues with the instruction ``offset`` away relative to itself.
- `jie r, offset`` is like ``jmp``, but only jumps if register ``r`` is even ("jump if even").
- `jio r, offset`` is like ``jmp``, but only jumps if register ``r`` is ``1`` ("jump if one", not odd).

All three jump instructions work with an offset relative to that instruction.
The offset is always written with a prefix ``+`` or ``-`` to indicate the direction of the jump
(forward or backward, respectively).
For example, ``jmp +1`` would simply continue with the next instruction,
while ``jmp +0`` would continuously jump back to itself forever.

The program exits when it tries to run an instruction beyond the ones defined.

For example, this program sets a to 2, because the jio instruction causes it to skip the tpl instruction::

	inc a
	jio a, +2
	tpl a
	inc a

What is the value in register ``b`` when the program in your puzzle input is finished executing?.
"""

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================


def run_program(reg_a=0, reg_b=0):

	cur = 0

	instructions = [x for x in PathPlus("input.txt").read_lines() if x]

	try:
		while True:
			instruction = instructions[cur]

			if instruction.startswith("hlf"):
				register = instruction[4]
				if register == 'a':
					reg_a = reg_a // 2
				elif register == 'b':
					reg_b = reg_b // 2
				else:
					raise RuntimeError
			elif instruction.startswith("tpl"):
				register = instruction[4]
				if register == 'a':
					reg_a = reg_a * 3
				elif register == 'b':
					reg_b = reg_b * 3
				else:
					raise RuntimeError
			elif instruction.startswith("inc"):
				register = instruction[4]
				if register == 'a':
					reg_a += 1
				elif register == 'b':
					reg_b += 1
				else:
					raise RuntimeError
			elif instruction.startswith("jmp"):
				cur += int(instruction[4:])
				continue
			elif instruction.startswith("jie"):
				register = instruction[4]
				offset = int(instruction[7:])
				if register == 'a':
					if not reg_a % 2:
						cur += int(offset)
						continue

				elif register == 'b':
					if not reg_b % 2:
						cur += int(offset)
						continue

				else:
					raise RuntimeError

			elif instruction.startswith("jio"):
				register = instruction[4]
				offset = int(instruction[7:])
				if register == 'a':
					if reg_a == 1:
						cur += int(offset)
						continue

				elif register == 'b':
					if reg_b == 1:
						cur += int(offset)
						continue

				else:
					raise RuntimeError

			cur += 1

	except IndexError:
		# print(cur, len(instructions), reg_a, reg_b)
		print(f"After the program exits, the value of register B is {reg_b}.")  # 184


run_program()

# ==========================
print("\nPart Two")
# ==========================
"""
The unknown benefactor is very thankful for releasi-- er,
helping little Jane Marie with her computer.
Definitely not to distract you, what is the value in register b after the program
is finished executing if register a starts as ``1`` instead?
"""

run_program(reg_a=1)  # 231
