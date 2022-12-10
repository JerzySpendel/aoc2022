from __future__ import annotations
import dataclasses
from typing import Iterable


@dataclasses.dataclass
class Dir:
    name: str | None
    parent: Dir | None
    files: list[int]
    dirs: list[Dir]

    def cd(self, dir_name) -> Dir:
        for dir in self.dirs:
            if dir.name == dir_name:
                return dir

    def size(self) -> int:
        size = sum(self.files)
        for dir in self.dirs:
            size += dir.size()
        return size

    def all_dirs(self) -> Iterable[Dir]:
        yield from self.dirs
        for dir in self.dirs:
            yield from dir.all_dirs()

    def __eq__(self, other):
        return other.name == self.name and other.parent == self.parent

    def __hash__(self):
        if not self.parent:
            return hash('/')

        parents = []
        parent = self
        while parent := parent.parent:
            parents.append(parent.name)
        return hash(tuple(parents))


root = Dir(dirs=[], files=[], parent=None, name='')
current_dir = root
for line in open('input', 'r').readlines():
    line = line.strip()
    splitted = line.split(' ')
    if line.startswith('$'):
        match splitted:
            case [_, 'cd', parameter]:
                if parameter == '/':
                    current_dir = root
                elif parameter == '..':
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir.cd(parameter)
            case [_, 'ls']:
                continue
    else:
        match splitted:
            case ['dir', name]:
                current_dir.dirs.append(
                    Dir(name=name, parent=current_dir, dirs=[], files=[])
                )
            case [size, filename]:
                current_dir.files.append(int(size))

correct_dirs = set()
for dir in root.all_dirs():
    if dir.size() <= 100000:
        correct_dirs.add(dir)


print(sum([dir.size() for dir in correct_dirs]))

total = 70000000
taken = root.size()
free = total - taken
to_delete = 30000000 - free

correct_to_delete = []
for dir in root.all_dirs():
    if (size := dir.size()) >= to_delete:
        correct_to_delete.append(size)

print(min(correct_to_delete))
