data = open('input').read()
for index, char in enumerate(data[:-14]):
    if len(set(data[index:index+14])) == 14:
        print(index + 14)
        break