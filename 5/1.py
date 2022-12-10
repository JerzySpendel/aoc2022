data = open('input', 'r').readlines()

stacks = []
for col in range(1, 36, 4):
    stack = []
    for row in range(8):
        try:
            if data[row][col] == ' ':
                continue
            stack.append(data[row][col])
        except IndexError:
            continue
    stacks.append(list(reversed(stack)))


for instruction in data[10:]:
    instruction_split = instruction.split(' ')
    amount, from_index, to_index = int(instruction_split[1]), int(instruction_split[3]) - 1, int(instruction_split[5]) - 1

    temp_stack = []
    for _ in range(amount):
        temp_stack.append(stacks[from_index].pop())

    for element in reversed(temp_stack):
        stacks[to_index].append(element)

for stack in stacks:
    print(stack[-1])