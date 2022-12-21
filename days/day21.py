import re

from lib.day import Day


class Day21(Day):
    def part1(self):
        dependents, known = self.parse_input()
        new_known = set(known.keys())

        while 'root' not in known:
            cursor_known = new_known
            new_known = set()
            for key in cursor_known:
                if key not in dependents:
                    continue

                target, a, b, operator = dependents[key]
                if a not in known or b not in known:
                    continue

                known[target] = operator(a, b)
                new_known.add(target)
        return known['root']

    def part2(self):
        pass

    def parse_input(self):
        dependent = dict()
        known = dict()
        for line in self.read_input().split('\n'):
            if line[6].isdigit():
                name, value = line.split(': ')
                known[name] = int(value)
                continue

            name, a, operator, b = re.search('(.+?): (.+?) ([+\\-*/]) (.+)', line).groups()
            if operator == '+':
                operator = lambda x, y: known[x] + known[y]
            elif operator == '-':
                operator = lambda x, y: known[x] - known[y]
            elif operator == '*':
                operator = lambda x, y: known[x] * known[y]
            elif operator == '/':
                operator = lambda x, y: known[x] // known[y]

            dependent[a] = (name, a, b, operator)
            dependent[b] = (name, a, b, operator)

        return dependent, known
