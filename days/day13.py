import functools

from lib.day import Day


class Day13(Day):

    def part1(self):
        result = 0
        for i, (left, right) in enumerate(self.parse_input()):
            if self.compare(left, right) >= 0:
                result += i + 1
        return result

    def part2(self):
        packets = [v for t in self.parse_input() for v in t]
        first, second = [[2]], [[6]]
        packets.append(first)
        packets.append(second)
        key = functools.cmp_to_key(lambda a, b: self.compare(a, b))
        packets.sort(key=key, reverse=True)
        return (packets.index(first) + 1) * (packets.index(second) + 1)

    def compare(self, left, right):
        if type(left) == int and type(right) == int:
            return 1 if left < right else (0 if left == right else -1)
        left = [left] if type(left) == int else left
        right = [right] if type(right) == int else right
        for item1, item2 in zip(left, right):
            comp = self.compare(item1, item2)
            if comp != 0:
                return comp
        if len(left) < len(right):
            return 1
        if len(left) > len(right):
            return -1
        return 0

    def parse_input(self):
        result = []
        for comb in self.read_input().split('\n\n'):
            left, right = comb.split('\n')
            left, right = eval(left), eval(right)
            result.append((left, right))
        return result
