def part1():
    system = read_input()
    print(sum([size[0] for size in system.values() if size[0] <= 100000]))


def part2():
    system = read_input()
    print(min([size[0] for size in system.values() if system['/'][0] - size[0] <= 40000000]))


def read_input():
    path = [[0]]
    absolute_path = '/'
    system = {absolute_path: path[-1]}
    for line in open('day7.txt').read().split('\n')[1:]:
        if line.startswith('$ ls'):
            pass
        elif line.startswith('dir'):
            system[absolute_path + '/' + line.split('dir ')[1]] = [0]
        elif line[0].isnumeric():
            size, name = tuple(line.split())
            size = int(size)
            for n in path:
                n[0] += size
        elif line.startswith('$ cd ..'):
            path.pop()
            absolute_path = absolute_path[:len(absolute_path) - absolute_path[::-1].index('/') - 1]
        elif line.startswith('$ cd'):
            name = line.split('$ cd ')[1]
            absolute_path += '/' + name
            path.append(system[absolute_path])
    return system


part1()
part2()
