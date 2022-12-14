from lib.day import Day


class Day14(Day):
    def part1(self):
        filled, source, highest_y = self.parse_input()
        result = 0
        x, y = source
        while y < highest_y:
            tx, ty = self.find_next(x, y, filled)
            if x == tx and y == ty:
                filled.add((x, y))
                result += 1
                x, y = source
            else:
                x, y = tx, ty
            if y >= highest_y:
                break
        return result

    def part2(self):
        filled, source, highest_y = self.parse_input()
        result = 0
        x, y = source
        while True:
            tx, ty = self.find_next(x, y, filled)
            if (tx, ty) == source:
                result += 1
                break

            if x == tx and y == ty or y == highest_y + 1:
                filled.add((x, y))
                result += 1
                x, y = source
            else:
                x, y = tx, ty
        return result

    def find_next(self, x, y, filled):
        if (x, y + 1) not in filled:
            return (x, y + 1)
        elif (x - 1, y + 1) not in filled:
            return (x - 1, y + 1)
        elif (x + 1, y + 1) not in filled:
            return (x + 1, y + 1)
        return (x, y)

    def parse_input(self):
        stone = set()
        source = (500, 0)
        highest_y = float('-inf')
        for line in self.read_input().split('\n'):
            points = [tuple(map(int, point.split(','))) for point in line.split(' -> ')]
            for (x1, y1), (x2, y2) in zip(points, points[1:]):
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    for y in range(min(y1, y2), max(y1, y2) + 1):
                        stone.add((x, y))
                        highest_y = max(highest_y, y)
        return stone, source, highest_y
