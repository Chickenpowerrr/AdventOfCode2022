import re

from lib.day import Day


class Day21(Day):
    def part1(self):
        dependents, known, _ = self.parse_input()
        return self.simulate(known, dependents)['root']

    def part2(self):
        dependents, start_known, (root_a, root_b) = self.parse_input()

        known = start_known.copy()
        known['humn'] = 0
        result = self.simulate(known, dependents)
        result = result[root_a], result[root_b]

        decreasing = result[0] > result[1]

        left_index = 0
        right_index = 100000000000000

        while True:
            if left_index > right_index:
                return None

            middle_index = (right_index + left_index) // 2
            known = start_known.copy()
            known['humn'] = middle_index
            result = self.simulate(known, dependents)
            result = result[root_a], result[root_b]

            if result[0] == result[1]:
                return middle_index

            if result[0] > result[1] and decreasing:
                left_index = middle_index + 1
            else:
                right_index = middle_index - 1


    def simulate(self, known, dependents):
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

                known[target] = operator(known[a], known[b])
                new_known.add(target)
        return known


    def parse_input(self):
        dependent = dict()
        known = dict()
        roots = None
        for line in self.read_input().split('\n'):
            if line[6].isdigit():
                name, value = line.split(': ')
                known[name] = int(value)
                continue

            name, a, operator, b = re.search('(.+?): (.+?) ([+\\-*/]) (.+)', line).groups()
            if operator == '+':
                operator = lambda x, y: x + y if type(x) == type(y) == int \
                    else f'({x} + {y})'
            elif operator == '-':
                operator = lambda x, y: x - y if type(x) == type(y) == int \
                    else f'({x} - {y})'
            elif operator == '*':
                operator = lambda x, y: x * y if type(x) == type(y) == int \
                    else f'({x} * {y})'
            elif operator == '/':
                operator = lambda x, y: x // y if type(x) == type(y) == int \
                    else f'({x} / {y})'

            dependent[a] = (name, a, b, operator)
            dependent[b] = (name, a, b, operator)

            if name == 'root':
                roots = a, b

        return dependent, known, roots
