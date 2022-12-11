import re
from functools import reduce

from lib.day import Day


class Day11(Day):
    def part1(self):
        items, operations = self.parse_input()
        inspections = [0 for _ in items]

        for _ in range(20):
            for monkey in range(len(items)):
                operation = operations[monkey]
                for _ in range(len(items[monkey])):
                    inspections[monkey] += 1
                    item = items[monkey].pop()
                    item = operation[0](item, operation[1])
                    item = item // 3
                    next_monkey = operation[3] if item % operation[2] == 0 else operation[4]
                    items[next_monkey].append(item)
        return reduce(lambda i, j: i * j, sorted(inspections)[-2:])

    def part2(self):
        items, operations = self.parse_input()
        inspections = [0 for _ in items]
        divisor = reduce(lambda i, j: i * j, [o[2] for o in operations])

        for r in range(10000):
            for monkey in range(len(items)):
                operation = operations[monkey]
                for _ in range(len(items[monkey])):
                    inspections[monkey] += 1
                    item = items[monkey].pop()
                    item = operation[0](item, operation[1])
                    item = item % divisor
                    next_monkey = operation[3] if item % operation[2] == 0 else operation[4]
                    items[next_monkey].append(item)
        return reduce(lambda i, j: i * j, sorted(inspections)[-2:])

    def parse_input(self):
        items = []
        operations = []
        for line in self.read_input().split('\n'):
            ints = [int(i) for i in re.findall('\\d+', line)]
            if 'Monkey' in line:
                operations.append([])
            elif 'Starting items' in line:
                items.append(ints)
            elif 'Operation' in line and '+' in line:
                operations[-1].append(lambda i, j: i + j)
                operations[-1].append(ints[0])
            elif 'Operation' in line and '*' in line and len(ints) > 0:
                operations[-1].append(lambda i, j: i * j)
                operations[-1].append(ints[0])
            elif 'Operation' in line and '*' in line:
                operations[-1].append(lambda i, j: i * i)
                operations[-1].append(0)
            elif 'Test' in line:
                operations[-1].append(ints[0])
            elif 'If true' in line:
                operations[-1].append(ints[0])
            elif 'If false' in line:
                operations[-1].append(ints[0])
        return items, operations

