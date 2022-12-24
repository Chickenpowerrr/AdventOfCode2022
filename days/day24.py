from queue import Queue

from lib.day import Day


class Day24(Day):
    def part1(self):
        start, end, walls, blizzards = self.parse_input()
        paths = Queue()
        paths.put((start, 0))
        highest_length = -1

        i = 0
        while paths.qsize() > 0:
            cursor, length = paths.get()

            if highest_length != length:
                highest_length = length
                print(f'{length}, {i}, {paths.qsize() + 1}')
                blizzards = self.advance_blizzards(blizzards, walls)

            if cursor == end:
                return length
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)):
                target = cursor[0] + dx, cursor[1] + dy
                if target in blizzards or (target in walls and not (start == cursor == target)):
                    i += 1
                    continue
                if cursor == start and ((dx, dy) == (0, -1)):
                    continue
                paths.put((target, length + 1))
        return float('inf')

    def part2(self):
        pass

    def advance_blizzards(self, blizzards, walls):
        next_blizzards = dict()
        for (x, y), deltas in blizzards.items():
            for (dx, dy) in deltas:
                nx, ny = x + dx, y + dy
                if (nx, ny) in walls:
                    max_x, max_y = max(x for x, _ in walls), max(y for _, y in walls)
                    if nx == 0 or ny == 0:
                        nx, ny = nx if nx != 0 else max_x - 1, ny if ny != 0 else max_y - 1
                    else:
                        nx, ny = nx if nx != max_x else 1, ny if ny != max_y else 1
                if (nx, ny) not in next_blizzards:
                    next_blizzards[(nx, ny)] = []
                next_blizzards[(nx, ny)].append((dx, dy))
        return next_blizzards

    def parse_input(self):
        walls = set()
        start = end = None
        blizzards = dict()

        for y, line in enumerate(self.read_input().split()):
            for x, character in enumerate(line):
                if character == '#':
                    walls.add((x, y))
                elif character == '.':
                    if start is None:
                        start = (x, y)
                        walls.add((x, y))
                    end = (x, y)
                elif character == '^':
                    blizzards[(x, y)] = [(0, -1)]
                elif character == '>':
                    blizzards[(x, y)] = [(1, 0)]
                elif character == 'v':
                    blizzards[(x, y)] = [(0, 1)]
                elif character == '<':
                    blizzards[(x, y)] = [(-1, 0)]
        return start, end, walls, blizzards

