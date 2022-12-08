def part1():
    input = parse_input()
    print(len([1 for row, l in enumerate(input) for column, level in enumerate(l)
               if check(input, row, column, level)]))


def part2():
    input = parse_input()
    print(max([view(input, row, column, level) for row, l in enumerate(input) for
               column, level in enumerate(l)]))


def parse_input():
    return [list(map(int, line)) for line in open('day8.txt').read().split()]


def check(input, row, column, level):
    if row == 0 or row == len(input) - 1 or column == 0 or column == len(input[row]) - 1:
        return True

    return all([input[r][column] < level for r in range(0, row)]) \
           or all([input[r][column] < level for r in range(row + 1, len(input))]) \
           or all([input[row][c] < level for c in range(0, column)]) \
           or all([input[row][c] < level for c in range(column + 1, len(input[row]))])


def view(input, row, column, level):
    if row == 0 or row == len(input) - 1 or column == 0 or column == len(input[row]) - 1:
        return 0

    p1 = 0
    for r in reversed(range(0, row)):
        p1 += 1
        if input[r][column] >= level:
            break

    p2 = 0
    for r in range(row + 1, len(input)):
        p2 += 1
        if input[r][column] >= level:
            break

    p3 = 0
    for c in reversed(range(0, column)):
        p3 += 1
        if input[row][c] >= level:
            break

    p4 = 0
    for c in range(column + 1, len(input[row])):
        p4 += 1
        if input[row][c] >= level:
            break

    return p1 * p2 * p3 * p4


part1()
part2()
