from lib.day import Day


class Day01(Day):
    def part1(self):
        return max(sum(map(int, elf.split('\n'))) for elf in self.read_input().split('\n\n'))

    def part2(self):
        return sum(sorted(sum(map(int, elf.split('\n')))
                          for elf in self.read_input().split('\n\n'))[-3:])
