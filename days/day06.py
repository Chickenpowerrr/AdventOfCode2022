from lib.day import Day


class Day06(Day):
    def part1(self):
        return self.solve(self.read_input(), 4)

    def part2(self):
        return self.solve(self.read_input(), 14)

    def solve(self, input, length):
        return min([i + 1 for i in range(3, len(input))
                   if len(set(input[i - length + 1:i + 1])) == length])
