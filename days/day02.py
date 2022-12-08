from lib.day import Day


class Day02(Day):
    def part1(self):
        score = 0
        for line in self.read_input().split():
            if 'X' in line:
                score += 1
                if 'A' in line:
                    score += 3
                elif 'B' in line:
                    score += 0
                elif 'C' in line:
                    score += 6
            elif 'Y' in line:
                score += 2
                if 'A' in line:
                    score += 6
                elif 'B' in line:
                    score += 3
                elif 'C' in line:
                    score += 0
            elif 'Z' in line:
                score += 3
                if 'A' in line:
                    score += 0
                elif 'B' in line:
                    score += 6
                elif 'C' in line:
                    score += 3
        return score

    def part2(self):
        score = 0
        for line in self.read_input().split():
            if 'X' in line:
                score += 0
                if 'A' in line:
                    score += 3
                elif 'B' in line:
                    score += 1
                elif 'C' in line:
                    score += 2
            elif 'Y' in line:
                score += 3
                if 'A' in line:
                    score += 1
                elif 'B' in line:
                    score += 2
                elif 'C' in line:
                    score += 3
            elif 'Z' in line:
                score += 6
                if 'A' in line:
                    score += 2
                elif 'B' in line:
                    score += 3
                elif 'C' in line:
                    score += 1
        return score
