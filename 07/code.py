"""
--- Day 7: Some Assembly Required ---

This year, Santa brought little Bobby Tables a set of wires and bitwise logic gates!
Unfortunately, little Bobby is a little under the recommended age range, and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit signal (a number from ``0`` to ``65535``).
A signal is provided to each wire by a gate, another wire, or some specific value.
Each wire can only get a signal from one source, but can provide its signal to multiple destinations.
A gate provides no signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts together:
``x AND y -> z`` means to connect wires ``x`` and ``y`` to an AND gate, and then connect its output to wire ``z``.

For example::

- ``123 -> x`` means that the signal ``123`` is provided to wire ``x``.
- ``x AND y -> z`` means that the bitwise AND of wire ``x`` and wire ``y`` is provided to wire ``z``.
- ``p LSHIFT 2 -> q`` means that the value from wire ``p`` is left-shifted by ``2`` and then provided to wire ``q``.
- ``NOT e -> f`` means that the bitwise complement of the value from wire ``e`` is provided to wire ``f``.

Other possible gates include ``OR`` (bitwise OR) and ``RSHIFT`` (right-shift).

For example, here is a simple circuit::

	123 -> x
	456 -> y
	x AND y -> d
	x OR y -> e
	x LSHIFT 2 -> f
	y RSHIFT 2 -> g
	NOT x -> h
	NOT y -> i

After it is run, these are the signals on the wires::

	d: 72
	e: 507
	f: 492
	g: 114
	h: 65412
	i: 65079
	x: 123
	y: 456

In little Bobby's kit's instructions booklet (provided as your puzzle input),
what signal is ultimately provided to wire ``a``?.
"""

# stdlib
from typing import List

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

gates = [x for x in PathPlus("input.txt").read_lines() if x]

OR = "OR"  # |
AND = "AND"  # &
NOT = "NOT"  # ~
RSHIFT = "RSHIFT"  # >>
LSHIFT = "LSHIFT"  # <<
ASSIGN = "->"


class Gate:

	def __init__(
			self,
			inputs: List[str],
			gate_type: str,
			output: str,
			):
		self.inputs: List[str] = inputs
		self.gate_type: str = gate_type
		self.output: str = output

	@classmethod
	def from_string(cls, string: str):
		tokens = string.split(' ')

		if tokens[0] == NOT:
			return cls(inputs=[tokens[1]], gate_type=NOT, output=tokens[-1])
		elif tokens[1] == OR:
			return cls(inputs=[tokens[0], tokens[2]], gate_type=OR, output=tokens[-1])
		elif tokens[1] == AND:
			return cls(inputs=[tokens[0], tokens[2]], gate_type=AND, output=tokens[-1])
		elif tokens[1] == RSHIFT:
			return cls(inputs=[tokens[0], tokens[2]], gate_type=RSHIFT, output=tokens[-1])
		elif tokens[1] == LSHIFT:
			return cls(inputs=[tokens[0], tokens[2]], gate_type=LSHIFT, output=tokens[-1])
		elif tokens[1] == ASSIGN:
			return cls(inputs=[tokens[0]], gate_type=ASSIGN, output=tokens[-1])

	def __repr__(self):
		if self.gate_type == NOT:
			return f"Gate(NOT {self.inputs[0]} -> {self.output})"
		elif self.gate_type == OR:
			return f"Gate({self.inputs[0]} OR {self.inputs[1]} -> {self.output})"
		elif self.gate_type == AND:
			return f"Gate({self.inputs[0]} AND {self.inputs[1]} -> {self.output})"
		elif self.gate_type == RSHIFT:
			return f"Gate({self.inputs[0]} RSHIFT {self.inputs[1]} -> {self.output})"
		elif self.gate_type == LSHIFT:
			return f"Gate({self.inputs[0]} LSHIFT {self.inputs[1]} -> {self.output})"
		elif self.gate_type == ASSIGN:
			return f"Gate({self.inputs[0]} -> {self.output})"

	def evaluate(self):
		if not all(x.isdigit() for x in self.inputs):
			return None

		if self.gate_type == ASSIGN:
			ret = int(self.inputs[0])
		elif self.gate_type == NOT:
			ret = ~int(self.inputs[0])
		elif self.gate_type == AND:
			ret = int(self.inputs[0]) & int(self.inputs[1])
		elif self.gate_type == OR:
			ret = int(self.inputs[0]) | int(self.inputs[1])
		elif self.gate_type == LSHIFT:
			ret = int(self.inputs[0]) << int(self.inputs[1])
		elif self.gate_type == RSHIFT:
			ret = int(self.inputs[0]) >> int(self.inputs[1])

		return abs(ret)


def evaluate_gates(gates):
	values = {}  # mapping of wire names to signal values
	gates = list(gates)

	while gates:
		for gate in gates:
			parsed_gate = Gate.from_string(gate)

			for wire, signal in values.items():
				if wire in parsed_gate.inputs:
					parsed_gate.inputs[parsed_gate.inputs.index(wire)] = str(signal)

			if all(x.isdigit() for x in parsed_gate.inputs):
				values[parsed_gate.output] = parsed_gate.evaluate()
				gates.remove(gate)

	return values


values = evaluate_gates(gates)

print("The signal on wire 'a' is:", values['a'])  # 3176

# ==========================
print("\nPart Two")
# ==========================
"""
Now, take the signal you got on wire ``a``, override wire ``b`` to that signal,
and reset the other wires (including wire ``a``). What new signal is ultimately provided to wire ``a``?
"""

gates[3] = f"{values['a']} -> b"

values = evaluate_gates(gates)

print("The signal on wire 'a' is:", values['a'])  # 14710
