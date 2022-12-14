import re

from lib.day import Day


class Day15(Day):
    def part1(self):
        target = 2000000
        ranges = []
        target_beacons = set()
        for x1, y1, x2, y2 in self.parse_input():
            distance = abs(x1 - x2) + abs(y1 - y2)
            if y2 == target:
                target_beacons.add(x2)
            if distance >= abs(y1 - target):
                radius = distance - abs(y1 - target)
                ranges.append(Range(x1 - radius, x1 + radius))
        if target != 2000000:
            print('TESTING ONLY, SET target=2000000 FOR REAL OUTPUT')
        return sum([len(r) for r in self.overlap_ranges(ranges)]) - len(target_beacons)

    def part2(self):
        width = 4000000
        targets = [(x1, y1, abs(x1 - x2) + abs(y1 - y2)) for x1, y1, x2, y2 in self.parse_input()]
        targets.sort(key=lambda i: i[2])

        for (x, y, length) in targets:
            a = self.test_ranges(length, targets, width, x, y - length - 1, +1, +1)
            b = self.test_ranges(length, targets, width, x + length + 1, y, -1, +1)
            c = self.test_ranges(length, targets, width, x, y + length + 1, -1, -1)
            d = self.test_ranges(length, targets, width, x - length - 1, y, +1, -1)

            if a is not None:
                return a[0] * width + a[1]
            if b is not None:
                return b[0] * width + b[1]
            if c is not None:
                return c[0] * width + c[1]
            if d is not None:
                return d[0] * width + d[1]

        if width != 4000000:
            print('TESTING ONLY, SET width=4000000 FOR REAL OUTPUT')
        return None

    def overlap_ranges(self, ranges):
        result = []
        updated = False
        while len(ranges) > 0:
            r1 = ranges.pop()
            cursor_updated = False
            for r2 in ranges:
                next_range = r1.union(r2)
                if next_range is not None:
                    ranges.remove(r2)
                    cursor_updated = True
                    result.append(next_range)
            if not cursor_updated:
                result.append(r1)
            updated = updated or cursor_updated

        if updated:
            return self.overlap_ranges(result)
        return result

    def parse_input(self):
        result = []
        for line in self.read_input().split('\n'):
            result.append(tuple(map(int, re.search('Sensor at x=(-?\\d+), y=(-?\\d+): '
                                                   'closest beacon is at '
                                                   'x=(-?\\d+), y=(-?\\d+)', line).groups())))
        return result

    def test_ranges(self, length, targets, width, tx, ty, dx, dy):
        for _ in range(length):
            if tx < 0 or ty < 0 or (tx > width and dx > 0) or (ty > width and dy > 0):
                break
            if not (0 <= tx <= width and 0 <= ty <= width):
                continue
            if all(map(lambda t: abs(tx - t[0]) + abs(ty - t[1]) > t[2], targets)):
                return tx, ty
            tx, ty = tx + dx, ty + dy
        return None


class Range:
    def __init__(self, start, end):
        self._start = start
        self._end = end

    def __len__(self):
        if self._start > self._end:
            return 0
        return self._end - self._start + 1

    def overlap(self, other: 'Range'):
        if other._start <= self._start <= other._end:
            return min(self._end, other._end) - self._start + 1
        if other._start <= self._end <= other._end:
            return self._end - max(self._start, other._start) + 1
        if self._start >= other._start and self._end <= other._end:
            return self._end - self._start + 1
        return 0

    def union(self, other: 'Range'):
        if other._start <= self._start <= other._end:
            return Range(other._start, max(self._end, other._end))
        if other._start <= self._end <= other._end:
            return Range(min(self._start, other._start), other._end)
        if self._start >= other._start and self._end <= other._end:
            return other
        return None

    def __str__(self):
        return f'[{self._start}, {self._end}]'
