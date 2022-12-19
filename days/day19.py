import re

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
        paths = [(next_robot, (0, 0, 0, 0), (1, 0, 0, 0), 0) for next_robot in range(4)
                 if self.can_buy_later((1, 0, 0, 0), costs[next_robot])]

        while len(paths) > 0:
            next_robot, resources, robots, minutes = paths.pop()
            print(f'{minutes}, {len(paths)}')

            if minutes == 24:
                max_geodes = max(max_geodes, resources[GEODE])
                continue

            if not self.can_buy_now(resources, costs[next_robot]):
                paths.append((next_robot, self.next_resources(resources, robots),
                              robots, minutes + 1))
                continue

            next_resources = tuple(resource - cost for resource, cost
                                   in zip(resources, costs[next_robot]))
            next_robots = tuple(resource + 1 if i == next_robot else resource
                                for i, resource in enumerate(resources))

            for next_robot in range(4):
                for next_next_robot, next_next_resources, next_next_robots \
                        in self.all_next_states(next_robot, next_resources, next_robots, costs):
                    paths.append((next_next_robot, next_next_resources,
                                  next_next_robots, minutes + 1))
        return max_geodes

    def all_next_states(self, next_robot, resources, robots, costs):
        if not self.can_buy_later(robots, costs[next_robot]):
            return set()

        if not self.can_buy_now(resources, costs[next_robot]):
            return {(next_robot, self.next_resources(resources, robots), robots)}

        result = set()
        next_resources = tuple(resource - cost for resource, cost
                               in zip(resources, costs[next_robot]))
        next_robots = tuple(resource + 1 if i == next_robot else resource
                            for i, resource in enumerate(resources))

        for next_robot in range(4):
            result = result.union(self.all_next_states(next_robot, next_resources,
                                                       next_robots, costs))
        return result

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
