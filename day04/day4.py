import re


def part1():
    print(len([1 for a, b, c, d
               in map(lambda line: map(int, re.split('[,-]', line)), open('day4.txt', 'r'))
               if (a <= c and b >= d) or (c <= a and b <= d)]))


def part2():
    print(len([1 for a, b, c, d
               in map(lambda line: map(int, re.split('[,-]', line)), open('day4.txt', 'r'))
               if a <= c <= b or a <= d <= b or c <= a <= d or c <= b <= d]))


part1()
part2()
