import re

from lib.day import Day


class Day16(Day):
    def part1(self):
        grid = self.parse_input()
        base_paths = {name: (0, set()) for name, (flow_rate, _) in grid.items()}
        optimal_paths = {-1: base_paths, -2: base_paths}

        for minutes_left in range(30):
            next_optimal_paths = {}
            optimal_paths[minutes_left] = next_optimal_paths

            for name, (total_flow, opened) in optimal_paths[minutes_left - 1].items():
                for other_name in grid[name][1]:
                    moving_flow = total_flow
                    opening_flow = optimal_paths[minutes_left - 2][other_name][0] \
                                   + minutes_left * grid[name][0] \
                        if other_name in optimal_paths[minutes_left - 2] else -1
                    if name not in opened and opening_flow > next_optimal_paths\
                            .get(name, (-1, ))[0]:
                        next_optimal_paths[name] = opening_flow, opened.union({name})
                    if moving_flow > next_optimal_paths.get(other_name, (-1, ))[0]:
                        next_optimal_paths[other_name] = moving_flow, opened

        # BB, CC, DD, EE, HH, and JJ
        return optimal_paths[29]

    def part2(self):
        pass

    def parse_input(self):
        values = dict()
        for line in self.read_input().split('\n'):
            pattern = re.search('Valve (.+) has flow rate=(\\d+); tunnels? leads? to valves? (.+)', line)
            source = pattern.group(1)
            values[source] = (int(pattern.group(2)), values.get(source, (-1, set()))[1])
            for target in pattern.group(3).split(', '):
                flow, predecessors = values.get(target, (-1, set()))
                predecessors.add(source)
                values[target] = (flow, predecessors)
        print(values)
        return values
