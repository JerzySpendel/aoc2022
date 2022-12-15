from __future__ import annotations
from dataclasses import dataclass

class Knot:
    def __init__(self, position: tuple, child: Knot | None = None, parent: Knot | None = None):
        self.position = position
        self.child = child
        self.parent = parent

        self.positions = set()

    def update(self):
        if self.is_stable():
            return

        difference = (self.parent.position[0] - self.position[0], self.parent.position[1] - self.position[1])
        normalized = (difference[0] / abs(difference[0]) if difference[0] != 0 else 0, difference[1] / abs(difference[1]) if difference[1] != 0 else 0)
        self.position = (self.position[0] + normalized[0], self.position[1] + normalized[1])

        self.positions.add(self.position)
        if self.child:
            self.child.update()

    def is_stable(self):
        """
        Cannot be any closer to the parent
        """
        return (self.position[0] - self.parent.position[0])**2 + (self.position[1] - self.parent.position[1])**2 <= 2

    def move(self, instruction):
        MOVE_TABLE = {
            'U': (0, 1),
            'R': (1, 0),
            'D': (0, -1),
            'L': (-1, 0),
        }
        direction, value = instruction.split(' ')
        value = int(value)

        DS = (self.position[0] + MOVE_TABLE[direction][0] * value, self.position[1] + MOVE_TABLE[direction][1] * value)

        while self.position != DS:
            step = MOVE_TABLE[direction]
            self.position = (self.position[0] + step[0], self.position[1] + step[1])
            self.child.update()


class Bridge:
    def __init__(self):
        self.knots = []
        for _ in range(9):
            if self.knots:
                parent = self.knots[-1]
            else:
                parent = Knot((0, 0))
                self.knots.append(parent)

            child_knot = Knot((0, 0), None, parent)
            parent.child = child_knot

            self.knots.append(child_knot)

            
bridge = Bridge()
for instruction in open('../input').readlines():
    first = bridge.knots[0]
    instruction = instruction.strip()
    first.move(instruction)

print(len(bridge.knots[9].positions))