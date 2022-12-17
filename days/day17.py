from lib.day import Day


class Day17(Day):
    SHAPES = [{(0, 0), (1, 0), (2, 0), (3, 0)},
              {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
              {(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)},
              {(0, 0), (0, 1), (0, 2), (0, 3)},
              {(0, 0), (1, 0), (0, 1), (1, 1)}]

    def part1(self):
        grid = set()
        blows = self.parse_input()

        blow_index = 0
        for i in range(2022):
            print(i)
            shape = self.SHAPES[i % len(self.SHAPES)]
            shape = self.start_position(shape, grid)
            updated = True
            while updated:
                shape = self.blow(shape, blows[blow_index], grid)
                updated, shape = self.fall(shape, grid)
                blow_index = (blow_index + 1) % len(blows)
            grid = grid.union(shape)
        return -min(y for _, y in grid) + 1

    def part2(self):
        pass

    def blow(self, shape, action, grid):
        next_shape = {(x + (-1 if action else 1), y) for x, y in shape}
        if min([x for x, _ in next_shape]) < 0 or max([x for x, _ in next_shape]) >= 7:
            return shape
        if len(next_shape.union(grid)) < len(shape) + len(grid):
            return shape
        return next_shape

    def fall(self, shape, grid):
        next_shape = {(x, y + 1) for x, y in shape}
        if len(next_shape.union(grid)) < len(shape) + len(grid) \
                or max(y for _, y in next_shape) > 0:
            return False, shape
        return True, next_shape

    def start_position(self, shape, grid):
        grid_height = min({y for _, y in grid}) \
            if len(grid) > 0 else 1
        shape_height = max({y for _, y in shape})
        base = grid_height - shape_height
        return {(x + 2, base + y - 4) for x, y in shape}

    def parse_input(self):
        return list(map(lambda c: c == '<', self.read_input().replace('\r', '')))