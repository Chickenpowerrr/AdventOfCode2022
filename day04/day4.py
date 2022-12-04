def part1():
    result = 0
    for line in open('day4.txt', 'r').read().split('\n'):
        parts = line.split(',')
        a, b = tuple(map(int, parts[0].split('-')))
        c, d = tuple(map(int, parts[1].split('-')))

        if (a <= c and b >= d) or (c <= a and b <= d):
            result += 1
    print(result)


def part2():
    result = 0
    for line in open('day4.txt', 'r').read().split('\n'):
        parts = line.split(',')
        a, b = tuple(map(int, parts[0].split('-')))
        c, d = tuple(map(int, parts[1].split('-')))

        if a <= c <= b or a <= d <= b or c <= a <= d or c <= b <= d:
            result += 1
    print(result)


part1()
part2()
