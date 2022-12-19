import re
from collections import deque
from heapq import heappush, heappop
from math import ceil

from lib.day import Day


class Day19(Day):

    def part1(self):
        total = 0
        for i, costs in enumerate(self.parse_input(), 1):
            total += i * self.simulate(costs, 24)
        return total

    def part2(self):
        total = 1
        for i, costs in enumerate(self.parse_input()[:3], 1):
            total *= self.simulate(costs, 32)
        return total

    def simulate(self, costs, total_minutes):
        max_geodes = 0
        previous = set()
        paths = deque([((0, 0, 0, 0), (1, 0, 0, 0), 0)])

        while len(paths) > 0:
            resources, robots, minutes = paths.popleft()
            previous.add(robots)
            max_geodes = max(max_geodes, resources[-1])

            # Ignore path if there is one with more geode
            if max_geodes > resources[-1]:
                continue

            if minutes == total_minutes:
                continue

            for next_robot in range(5)[::-1]:
                if next_robot == 4:
                    next_resources = tuple(resource + robot
                                           for resource, robot in zip(resources, robots))
                    paths.append((next_resources, robots, minutes + 1))
                    continue

                if not self.can_buy(resources, costs[next_robot]):
                    continue

                next_robots = tuple(robot + 1 if i == next_robot else robot
                                    for i, robot in enumerate(robots))

                # Ignore bot executions that have already been explored
                if next_robots in previous:
                    continue

                next_resources = tuple(resource + robot - cost for resource, robot, cost
                                       in zip(resources, robots, costs[next_robot]))
                paths.append((next_resources, next_robots, minutes + 1))

                # Always take geode or obsidian
                if next_robot == 3:
                    break
        return max_geodes

    def can_buy(self, resources, costs):
        for resource, cost in zip(resources, costs):
            if resource < cost:
                return False
        return True

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
