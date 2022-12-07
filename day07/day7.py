def part1():
    pass


def part2():
    pass


def read_input():
    path = [{}]
    cursor = path[-1]
    system = {'/': cursor}
    for line in open('day7.txt').read().split('\n')[1:]:
        if line.startswith('$ ls'):
            pass
        elif line.startswith('dir'):
            cursor[line.split('dir ')[1]] = {}
        elif line[0].isnumeric():
            size, name = tuple(line.split())
            cursor[name] = int(size)
        elif line.startswith('$ cd ..'):
            path.pop()
            cursor = path[-1]
        elif line.startswith('$ cd'):
            name = line.split('$ cd ')[1]
            cursor = cursor[name]
            path.append(cursor)
    return system


part1()
part2()
