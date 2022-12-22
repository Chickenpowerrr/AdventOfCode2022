import re

from lib.day import Day

DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))


class Day22(Day):
    def part1(self):
        grid, path, (x, y) = self.parse_input()
        direction = DIRECTIONS[0]

        for action in path:
            if action == 'R':
                direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)]
                continue

            if action == 'L':
                direction = DIRECTIONS[DIRECTIONS.index(direction) - 1]
                continue

            for _ in range(action):
                x, y = self.next_tile(x, y, grid, direction[0], direction[1])

        return 1000 * y + 4 * x + DIRECTIONS.index(direction)

    def part2(self):
        pass

    def next_tile(self, x, y, grid, dx, dy):
        tx, ty = x + dx, y + dy
        if (tx, ty) in grid:
            return (tx, ty) if grid[(tx, ty)] else (x, y)

        if dx > 0:
            tx = min([x for x, y in grid if y == ty])
        elif dx < 0:
            tx = max([x for x, y in grid if y == ty])
        elif dy > 0:
            ty = min([y for x, y in grid if x == tx])
        elif dy < 0:
            ty = max([y for x, y in grid if x == tx])

        return (tx, ty) if grid[(tx, ty)] else (x, y)

    def parse_input(self):
        map_lines, path_line = tuple(self.read_input().split('\n\n'))

        grid = {}
        path = []
        start_column = float('inf')

        row = 1
        for line in map_lines.split('\n'):
            column = 1
            for character in line:
                if character != ' ':
                    grid[(column, row)] = character == '.'
                    if row == 1:
                        start_column = min(start_column, column)
                column += 1
            row += 1

        while len(path_line) > 0:
            if path_line[0].isalpha():
                path.append(path_line[0])
                path_line = path_line[1:]
                continue

            movements = re.search('(\\d+)', path_line).groups(1)[0]
            path.append(int(movements))
            path_line = path_line[len(movements):]

        return grid, path, (start_column, 1)
