import re

from lib.day import Day


class Day16(Day):
    def part1(self):
        grid = self.parse_input()
        edges = self.shortest_paths()

        best_scores = dict()
        best_path = float('-inf')
        paths = [('AA', 0, 0, frozenset())]

        while len(paths) > 0:
            cursor, minutes, total_flow, visited = paths.pop()
            best_path = max(best_path, total_flow)
            for (target, distance) in edges[cursor].items():
                next_targets = visited.union({target})
                next_total_flow = total_flow + grid[target][0] * (30 - minutes - distance)

                if best_scores.get(next_targets, float('-inf')) >= next_total_flow:
                    continue

                if target not in visited and distance + minutes < 30:
                    best_scores[next_targets] = next_total_flow
                    paths.append((target, distance + minutes,
                                  next_total_flow, visited.union({target})))
        return best_path

    def shortest_paths(self):
        grid = self.parse_input()
        result = {key: ({key: 1} if grid[key][0] > 0 else {}) for key in grid.keys()}
        for _ in range(len(grid)):
            for name, (_, next_names) in grid.items():
                for next_name in next_names:
                    for trans_name, trans_price in result[next_name].items():
                        result[name][trans_name] = \
                            min(result[name].get(trans_name, float('inf')), trans_price + 1)
        return result

    def part2(self):
        grid = self.parse_input()
        edges = self.shortest_paths()

        best_scores = dict()
        best_path = float('-inf')
        paths = [('AA', 'AA', 0, 0, 0, frozenset())]

        while len(paths) > 0:
            cursor_a, cursor_b, minutes_a, minutes_b, total_flow, visited = paths.pop()
            best_path = max(best_path, total_flow)
            for (target, distance) in edges[cursor_a].items():
                next_targets = visited.union({target})
                next_total_flow = total_flow + grid[target][0] * (26 - minutes_a - distance)

                if best_scores.get(next_targets, float('-inf')) >= next_total_flow:
                    continue

                if target not in visited and distance + minutes_a < 26:
                    best_scores[next_targets] = next_total_flow
                    paths.append((target, cursor_b, distance + minutes_a, minutes_b,
                                  next_total_flow, visited.union({target})))

            for (target, distance) in edges[cursor_b].items():
                next_targets = visited.union({target})
                next_total_flow = total_flow + grid[target][0] * (26 - minutes_b - distance)

                if best_scores.get(next_targets, float('-inf')) >= next_total_flow:
                    continue

                if target not in visited and distance + minutes_b < 26:
                    best_scores[next_targets] = next_total_flow
                    paths.append((cursor_a, target, minutes_a, distance + minutes_b,
                                  next_total_flow, visited.union({target})))
        return best_path


    def parse_input(self):
        values = dict()
        for line in self.read_input().split('\n'):
            pattern = re.search('Valve (.+) has flow rate=(\\d+); tunnels? leads? to valves? (.+)', line)
            values[pattern.group(1)] = (int(pattern.group(2)), pattern.group(3).split(', '))
        return values
