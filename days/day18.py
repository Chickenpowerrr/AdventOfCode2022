from collections import deque

from lib.day import Day


class Day18(Day):
    def part1(self):
        cubes = set(self.parse_input())
        total = 0
        for (x1, y1, z1) in cubes:
            for (dx, dy, dz) in ((-1, 0, 0), (1, 0, 0), (0, -1, 0),
                                 (0, 1, 0), (0, 0, -1), (0, 0, 1)):
                x2, y2, z2 = x1 + dx, y1 + dy, z1 + dz
                if (x2, y2, z2) not in cubes:
                    total += 1
        return total

    def part2(self):
        cubes = set(self.parse_input())
        surface = {}
        for (x1, y1, z1) in cubes:
            for (dx, dy, dz) in ((-1, 0, 0), (1, 0, 0), (0, -1, 0),
                                 (0, 1, 0), (0, 0, -1), (0, 0, 1)):
                x2, y2, z2 = x1 + dx, y1 + dy, z1 + dz
                if (x2, y2, z2) not in cubes:
                    if (x2, y2, z2) not in surface:
                        surface[(x2, y2, z2)] = 0
                    surface[(x2, y2, z2)] += 1

        total = 0
        reachable = self.external(cubes)
        for cube, occurrences in surface.items():
            if cube in reachable:
                total += occurrences
        return total

    def external(self, cubes):
        min_x, min_y, min_z = min(c[0] for c in cubes) - 1, \
                              min(c[1] for c in cubes) - 1, \
                              min(c[2] for c in cubes) - 1

        max_x, max_y, max_z = max(c[0] for c in cubes) + 1, \
                              max(c[1] for c in cubes) + 1, \
                              max(c[2] for c in cubes) + 1
        visited = set()
        to_visit = deque([(min_x, min_y, min_z)])
        while len(to_visit) > 0:
            x1, y1, z1 = to_visit.pop()
            visited.add((x1, y1, z1))
            for (dx, dy, dz) in ((-1, 0, 0), (1, 0, 0), (0, -1, 0),
                                 (0, 1, 0), (0, 0, -1), (0, 0, 1)):
                x2, y2, z2 = x1 + dx, y1 + dy, z1 + dz
                if min_x <= x2 <= max_x and min_y <= y2 <= max_y and min_z <= z2 <= max_z \
                        and (x2, y2, z2) not in visited and (x2, y2, z2) not in cubes:
                    to_visit.append((x2, y2, z2))
        return visited

    def parse_input(self):
        return [tuple(map(int, line.split(','))) for line in self.read_input().split()]
