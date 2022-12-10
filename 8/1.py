import dataclasses
import operator
from functools import reduce

data = open('input', 'r').readlines()
data = [line.strip() for line in data]


@dataclasses.dataclass
class Tree:
    height: int
    neighbours: list[int]

    def visible(self) -> bool:
        return any((neighbour < self.height for neighbour in self.neighbours))


trees: list[Tree] = []
count = 0
all_parts = []
for row in range(5):
    for col in range(5):

        current_tree = (row, col)
        current_height = int(data[row][col])
        visible = False
        parts = []
        directions =[(-1, 0), (1, 0), (0, 1), (0, -1)]
        for direction in directions:
            current = current_tree
            part_score = 0
            while True:
                match current:
                    case [0, _] | [_, 0] | [5, _] | [_, 5] as end:
                        break
                    case [checking_row, checking_col] as checking:
                        part_score += 1
                        if checking != current_tree and int(data[checking_row][checking_col]) >= current_height:
                            break

                current = (current[0] + direction[0], current[1] + direction[1])
            parts.append(part_score)
        all_parts.append(reduce(operator.mul, parts))

print(max(all_parts))