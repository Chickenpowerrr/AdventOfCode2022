import re

from lib.day import Day


class Day04(Day):
    def part1(self):
        return len([1 for a, b, c, d
                   in map(lambda line: map(int, re.split('[,-]', line)),
                          self.read_input().split())
                   if (a <= c and b >= d) or (c <= a and b <= d)])

    def part2(self):
        return len([1 for a, b, c, d
                   in map(lambda line: map(int, re.split('[,-]', line)),
                          self.read_input().split())
                   if a <= c <= b or a <= d <= b or c <= a <= d or c <= b <= d])
