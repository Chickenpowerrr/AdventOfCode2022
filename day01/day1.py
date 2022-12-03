def part1():
    print(max(sum(map(int, elf.split('\n'))) for elf in open('day1.txt', 'r').read().split('\n\n')))


def part2():
    print(sum(sorted(sum(map(int, elf.split('\n')))
                     for elf in open('day1.txt', 'r').read().split('\n\n'))[-3:]))


part1()
part2()
