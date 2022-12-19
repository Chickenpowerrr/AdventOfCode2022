import re
from math import ceil

from lib.day import Day

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3


class Day19(Day):

    def part1(self):
        return self.simulate(self.parse_input()[0])

    def part2(self):
        pass

    def simulate(self, costs):
        max_geodes = 0
        explored = {((0, 0, 0, 0), (1, 0, 0, 0), 0)}
        paths = [((0, 0, 0, 0), (1, 0, 0, 0), 0)]

        i = 0
        while len(paths) > 0:
            i += 1
            if i % 10000 == 0:
                print(f'{max_geodes}, {len(paths)}')

            resources, robots, minutes = paths.pop()
            max_geodes = max(max_geodes, resources[-1])

            for next_robot in range(4):
                distance = self.get_distance(resources, robots, costs[next_robot])
                if minutes + distance >= 23:
                    continue

                next_resources = tuple(resource + distance * robot - cost
                                       for resource, robot, cost
                                       in zip(resources, robots, costs[next_robot]))
                next_robots = tuple(robot + 1 if i == next_robot else robot
                                    for i, robot in enumerate(robots))
                next_path = (next_resources, next_robots, minutes + distance)

                if next_path not in explored:
                    paths.append(next_path)
                    explored.add(next_path)
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

    def next_resources(self, resources, robots):
        return tuple(resource + robot for resource, robot in zip(resources, robots))

    def can_buy_now(self, resources, cost):
        return all([resources[i] >= amount for i, amount in enumerate(cost)])

    def can_buy_later(self, robots, cost):
        return all([robots[i] > 0 or amount == 0 for i, amount in enumerate(cost)])

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
