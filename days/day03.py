import string
from functools import reduce
from iteration_utilities import grouper

from lib.day import Day


class Day03(Day):
    def part1(self):
        return sum([sum({1 + string.ascii_letters.find(c) for c in
                         {c for c in line[:len(line) // 2]}
                        .intersection({c for c in line[len(line) // 2:]})})
                    for line in self.read_input().split()])

    def part2(self):
        return sum([sum({1 + string.ascii_letters.find(c) for c in
                         reduce(lambda s1, s2: s1.intersection(s2), map(set, group))})
                    for group in
                    grouper(map(lambda l: l.strip(), self.read_input().split()), 3)])
