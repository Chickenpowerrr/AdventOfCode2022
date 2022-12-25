from lib.day import Day


class Day25(Day):

    def part1(self):
        return self.to_snafu(sum(map(self.parse_snafu, self.read_input().split())))

    def part2(self):
        return 'No Part 2 on Day 25 :)'

    def parse_snafu(self, number):
        result = 0
        for i, character in enumerate(number[::-1]):
            if character == '-':
                character = '-1'
            elif character == '=':
                character = '-2'
            result += pow(5, i) * int(character)
        return result

    def to_snafu(self, decimal):
        result = ''
        while decimal > 0:
            target = decimal % 5
            decimal //= 5

            if target == 3:
                result = f'={result}'
                decimal += 1
            elif target == 4:
                result = f'-{result}'
                decimal += 1
            else:
                result = f'{target}{result}'
        return result if len(result) > 0 else 0

