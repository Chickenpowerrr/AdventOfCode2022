import re
from math import ceil

from lib.day import Day


class Day19(Day):

    def part1(self):
        total = 0
        for i, costs in enumerate(self.parse_input(), 1):
            print(f'Starting: {i}')
            total += i * self.simulate(costs, 24)
        return total

    def part2(self):
        total = 0
        for i, costs in enumerate(self.parse_input(), 1):
            print(f'Starting: {i}')
            total += i * self.simulate(costs, 32)
        return total

    def simulate(self, costs, total):
        max_geodes = 0
        previous = {((0, 0, 0, 0), (1, 0, 0, 0), 0)}
        paths = [((0, 0, 0, 0), (1, 0, 0, 0), 0)]

        while len(paths) > 0:
            resources, robots, minutes = paths.pop()
            max_geodes = max(max_geodes, resources[-1])

            for next_robot in range(4):
                if self.could_buy_previously(resources, robots, costs[next_robot]):
                    continue

                distance = self.get_distance(resources, robots, costs[next_robot])

                if minutes + distance + 1 >= total:
                    max_geodes = max(max_geodes, resources[-1] + (total - minutes) * robots[-1])
                    continue

                next_resources = tuple(resource + (distance + 1) * robot - cost
                                       for resource, robot, cost
                                       in zip(resources, robots, costs[next_robot]))
                next_robots = tuple(robot + 1 if i == next_robot else robot
                                    for i, robot in enumerate(robots))
                next_path = (next_resources, next_robots, minutes + distance + 1)

                if next_path not in previous:
                    paths.append(next_path)
                    previous.add(next_path)
        return max_geodes

    def get_distance(self, resources, robots, costs):
        maximum = 0
        for resource, robot, cost in zip(resources, robots, costs):
            if cost > 0 and robot == 0:
                return float('inf')
            if cost == 0 and robot == 0:
                continue
            maximum = max(maximum, ceil((cost - resource) / robot))
        return maximum

    def could_buy_previously(self, resources, robots, costs):
        return all([resource - robot >= cost for resource, robot, cost
                    in zip(resources, robots, costs)])

    def parse_input(self):
        result = []
        for line in self.read_input().replace('\n', '') \
                            .replace('Blueprint', '\nBlueprint').split('\n')[1:]:
            parts = re.search("Blueprint \\d+:\\s+Each ore robot costs (.+?)\\.\\s+"
                              "Each clay robot costs (.+?)\\.\\s+"
                              "Each obsidian robot costs (.+?)\\.\\s+"
                              "Each geode robot costs (.+?)\\.", line).groups()
            result.append([self.parse_cost(part) for part in parts])
        return result

    def parse_cost(self, string):
        ore = re.search("(\\d+) ore", string)
        clay = re.search("(\\d+) clay", string)
        obsidian = re.search("(\\d+) obsidian", string)
        return int(ore.group(1)) if ore else 0, \
               int(clay.group(1)) if clay else 0, \
               int(obsidian.group(1)) if obsidian else 0, 0
