import re
from typing import Tuple, List

from lib.day import Day


class Day05(Day):
    def part1(self):
        stacks, instructions = self.parse_input()
        for amount, source, target in instructions:
            for _ in range(amount):
                stacks[target - 1].append(stacks[source - 1].pop())
        return ''.join([s[-1] for s in stacks])

    def part2(self):
        stacks, instructions = self.parse_input()
        for amount, source, target in instructions:
            index = len(stacks[source - 1]) - amount
            stacks[target - 1].extend(stacks[source - 1][index:])
            stacks[source - 1] = stacks[source - 1][:index]
        return ''.join([s[-1] for s in stacks])

    def parse_input(self) -> Tuple[List[List[str]], List[Tuple[int, int, int]]]:
        stack_lines, instruction_lines = tuple([line for line in lines.split('\n')]
                                               for lines
                                               in self.read_input().split('\n\n'))
        stacks = [[] for _ in stack_lines[-1].split('   ')]

        for line in stack_lines[-2::-1]:
            for i in range(len(stacks)):
                target = 1 + 4 * i
                if target < len(line) and line[target] != ' ':
                    stacks[i].append(line[target])

        instructions = [tuple(map(int, re.findall('\\d+', line))) for line in instruction_lines]

        return stacks, instructions
