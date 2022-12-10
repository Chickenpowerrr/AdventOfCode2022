from lib.day import Day


class Day10(Day):
    def part1(self):
        values = [1, 1]
        for value in self.parse_input():
            values.append(values[-1] + value)
        return sum(i * values[i] for i in (20, 60, 100, 140, 180, 220))

    def part2(self):
        result = ''
        sprite = 1
        instructions = self.parse_input()
        for row in range(6):
            current = ''
            for column in range(40):
                current += '#' if abs(sprite - column) <= 1 else '.'
                instruction = instructions[40 * row + column]
                sprite += instruction
            result += '\n'
            result += current
        return result

    def parse_input(self):
        instructions = []
        for line in self.read_input().split('\n'):
            instructions.append(0)
            if line.startswith('addx'):
                instructions.append(int(line.split()[1]))
        return instructions
