import string
from functools import reduce
from iteration_utilities import grouper


def part1():
    print(sum([sum({1 + (string.ascii_lowercase + string.ascii_uppercase).find(c) for c in
                    {c for c in line[:len(line) // 2]}
                   .intersection({c for c in line[len(line) // 2:]})})
               for line in open('day3.txt', 'r')]))


def part2():
    print(sum([sum({1 + (string.ascii_lowercase + string.ascii_uppercase).find(c) for c in
                    reduce(lambda s1, s2: s1.intersection(s2), map(set, group))})
               for group in grouper(map(lambda l: l.strip(), open('day3.txt', 'r')), 3)]))


part1()
part2()
