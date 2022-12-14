from heapq import heappop, heappush

from lib.day import Day


class Day24(Day):
    def part1(self):
        start, end, walls, start_blizzards = self.parse_input()
        return self.find_path(start, end, walls, start_blizzards)[0]

    def part2(self):
        start, end, walls, start_blizzards = self.parse_input()
        first_length, start_blizzards = self.find_path(start, end, walls, start_blizzards)
        second_length, start_blizzards = self.find_path(end, start, walls, start_blizzards)
        third_length, start_blizzards = self.find_path(start, end, walls, start_blizzards)
        return first_length + second_length + third_length

    def find_path(self, start, end, walls, start_blizzards):
        paths = [(self.manhattan_distance(start, end), 0, start)]
        blizzards = [start_blizzards]

        visited = dict()

        while len(paths) > 0:
            _, length, cursor = heappop(paths)

            if length not in visited:
                visited[length] = set()

            if cursor in visited[length]:
                continue

            visited[length].add(cursor)

            if len(blizzards) <= length + 1:
                blizzards.append(self.advance_blizzards(blizzards[-1], walls))

            if cursor == end:
                return length, blizzards[length]
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)):
                target = cursor[0] + dx, cursor[1] + dy
                if target in blizzards[length + 1] or target in walls:
                    continue
                heappush(paths, (length + 1 + self.manhattan_distance(target, end),
                                 length + 1, target))
        return float('inf'), start_blizzards

    def manhattan_distance(self, first, second):
        return abs(first[0] - second[0]) + abs(first[1] - second[1])

    def advance_blizzards(self, blizzards, walls):
        next_blizzards = dict()
        for (x, y), deltas in blizzards.items():
            for (dx, dy) in deltas:
                nx, ny = x + dx, y + dy
                if (nx, ny) in walls:
                    max_x, max_y = max(x for x, _ in walls), max(y for _, y in walls) - 1
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
                    end = (x, y)
                elif character == '^':
                    blizzards[(x, y)] = [(0, -1)]
                elif character == '>':
                    blizzards[(x, y)] = [(1, 0)]
                elif character == 'v':
                    blizzards[(x, y)] = [(0, 1)]
                elif character == '<':
                    blizzards[(x, y)] = [(-1, 0)]
        walls.add((start[0], start[1] - 1))
        walls.add((end[0], end[1] + 1))
        return start, end, walls, blizzards

