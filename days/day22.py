import re

from lib.day import Day

DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
EXAMPLE_CUBE_ADJACENT = {0: ((5, 2), (3, 0), (2, 1), (1, 2)),
                         1: ((2, 0), (4, 2), (5, 3), (0, 2)),
                         2: ((3, 0), (4, 1), (1, 0), (0, 3)),
                         3: ((5, 3), (3, 0), (2, 0), (0, 0)),
                         4: ((5, 0), (1, 2), (2, 3), (3, 0)),
                         5: ((0, 2), (1, 1), (4, 0), (3, 1))}
EXAMPLE_RELATIVE_POSITIONS = {0: (2, 0), 1: (0, 1), 2: (1, 1), 3: (2, 1), 4: (2, 2), 5: (3, 2)}

INPUT_CUBE_ADJACENT = {0: ((1, 0), (2, 0), (3, 2), (5, 3)),
                       1: ((4, 2), (2, 3), (0, 0), (5, 0)),
                       2: ((1, 1), (4, 0), (3, 1), (0, 0)),
                       3: ((4, 0), (5, 0), (0, 2), (2, 3)),
                       4: ((1, 2), (5, 3), (3, 0), (2, 0)),
                       5: ((4, 1), (1, 0), (0, 1), (3, 0))}
INPUT_RELATIVE_POSITIONS = {0: (1, 0), 1: (2, 0), 2: (1, 1), 3: (0, 2), 4: (1, 2), 5: (0, 3)}

class Day22(Day):

    def part1(self):
        grid, path, (x, y) = self.parse_first_input()
        direction = DIRECTIONS[0]

        for action in path:
            if action == 'R':
                direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)]
                continue

            if action == 'L':
                direction = DIRECTIONS[DIRECTIONS.index(direction) - 1]
                continue

            for _ in range(action):
                x, y = self.next_tile_first(x, y, grid, direction[0], direction[1])

        return 1000 * y + 4 * x + DIRECTIONS.index(direction)

    def part2(self):
        grid, path, dimension = self.parse_second_input()
        index = 0
        x, y = 1, 1
        direction = DIRECTIONS[0]

        for action in path:
            if action == 'R':
                direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)]
                continue

            if action == 'L':
                direction = DIRECTIONS[DIRECTIONS.index(direction) - 1]
                continue

            for _ in range(action):
                px, py, pindex = x, y, index
                x, y, index, dx, dy = self.next_tile_second(x, y, grid, direction[0], direction[1],
                                                            index, dimension, INPUT_CUBE_ADJACENT)
                direction = dx, dy

                if x == px and y == py and index == pindex:
                    break

        rx, ry = INPUT_RELATIVE_POSITIONS[index]
        x, y = x + rx * dimension, y + ry * dimension
        return 1000 * y + 4 * x + DIRECTIONS.index(direction)

    def next_tile_first(self, x, y, grid, dx, dy):
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

    def parse_first_input(self):
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

    def next_tile_second(self, x, y, grid, dx, dy, index, dimension, cube_adjacent):
        tx, ty, tindex = x + dx, y + dy, index
        if (tx, ty) in grid[index]:
            return (tx, ty, index, dx, dy) if grid[index][(tx, ty)] else (x, y, index, dx, dy)

        direction = 0
        if dx > 0:
            tindex, direction = cube_adjacent[index][0]
        elif dx < 0:
            tindex, direction = cube_adjacent[index][2]
        elif dy > 0:
            tindex, direction = cube_adjacent[index][1]
        elif dy < 0:
            tindex, direction = cube_adjacent[index][3]

        if direction == 0 and dy != 0:
            tx, ty = tx, 1 if dy > 0 else dimension
        elif direction == 0 and dx != 0:
            tx, ty = 1 if dx > 0 else dimension, ty
        elif direction == 1 and dx != 0:
            tx, ty = y, dimension if dx > 0 else 1
        elif direction == 1 and dy != 0:
            tx, ty = 1 if dy > 0 else dimension, dimension - tx + 1
        elif direction == 2 and dy != 0:
            tx, ty = dimension - tx + 1, dimension if dy > 0 else 1
        elif direction == 2 and dx != 0:
            tx, ty = dimension if dx > 0 else 1, dimension - ty + 1
        elif direction == 3 and dx != 0:
            tx, ty = dimension - ty + 1, 1 if dx > 0 else dimension
        elif direction == 3 and dy != 0:
            tx, ty = dimension if dy > 0 else 1, tx

        tdx, tdy = dx, dy
        if direction == 1:
            tdx, tdy = dy, -dx
        elif direction == 2:
            tdx, tdy = -dx, -dy
        elif direction == 3:
            tdx, tdy = -dy, dx

        if not grid[tindex][(tx, ty)]:
            return x, y, index, dx, dy
        return tx, ty, tindex, tdx, tdy

    def parse_second_input(self):
        map_lines, path_line = tuple(self.read_input().split('\n\n'))
        map_lines = map_lines.split('\n')
        dimension = max([max(x, y) for x, y in self.parse_first_input()[0]]) // 4

        index = 0
        grid = {}
        path = []

        for i in range(0, len(map_lines), dimension):
            for j in range(0, len(map_lines[i]), dimension):
                if map_lines[i][j] == ' ':
                    continue

                cursor_grid = {}

                row = 1
                for line in map_lines[i:i + dimension]:
                    column = 1
                    for character in line[j:j + dimension]:
                        if character != ' ':
                            cursor_grid[(column, row)] = character == '.'
                        column += 1
                    row += 1

                grid[index] = cursor_grid
                index += 1

        while len(path_line) > 0:
            if path_line[0].isalpha():
                path.append(path_line[0])
                path_line = path_line[1:]
                continue

            movements = re.search('(\\d+)', path_line).groups(1)[0]
            path.append(int(movements))
            path_line = path_line[len(movements):]

        return grid, path, dimension
