import re

from lib.day import Day


class Day16(Day):
    def part1(self):
        grid = self.parse_input()
        paths = [('AA', 0, 0, set())]

        for minute in range(30, 0, -1):
            print(minute)
            next_paths = []
            for cursor, total_flow, flow_per_second, opened in paths:
                total_flow += flow_per_second
                if cursor not in opened and grid[cursor][0] > 0:
                    next_paths.append((cursor, total_flow,
                                       flow_per_second + grid[cursor][0], opened.union({cursor})))
                for next_place in grid[cursor][1]:
                    next_paths.append((next_place, total_flow, flow_per_second, opened))
            paths = next_paths
        return paths

    def part2(self):
        pass

    def parse_input(self):
        values = dict()
        for line in self.read_input().split('\n'):
            pattern = re.search('Valve (.+) has flow rate=(\\d+); tunnels? leads? to valves? (.+)', line)
            values[pattern.group(1)] = (int(pattern.group(2)), pattern.group(3).split(', '))
        return values
