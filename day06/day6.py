def part1():
    print(solve(open('day6.txt').read(), 4))


def part2():
    print(solve(open('day6.txt').read(), 14))


def solve(input, length):
    return min([i + 1 for i in range(3, len(input))
               if len(set(input[i - length + 1:i + 1])) == length])


part1()
part2()
