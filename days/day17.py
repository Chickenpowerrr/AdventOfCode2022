from lib.day import Day


class Day17(Day):
    SHAPES = [{(0, 0), (1, 0), (2, 0), (3, 0)},
              {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
              {(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)},
              {(0, 0), (0, 1), (0, 2), (0, 3)},
              {(0, 0), (1, 0), (0, 1), (1, 1)}]

    def part1(self):
        return self.simulate(set(), 2022)

    def part2(self):
        grid = set()
        blows = self.parse_input()
        encountered = dict()

        blow_index = 0
        for i in range(1000000000000):
            before_height = 1 - (min(y for _, y in grid) if len(grid) > 0 else 1)
            before_grid = grid
            before_blow_index = blow_index

            shape = self.SHAPES[i % len(self.SHAPES)]
            shape = self.start_position(shape, grid)
            updated = True
            while updated:
                shape = self.blow(shape, blows[blow_index], grid)
                updated, shape = self.fall(shape, grid)
                blow_index = (blow_index + 1) % len(blows)
            grid = grid.union(shape)

            current = (i % len(self.SHAPES), blow_index, self.get_shape(grid))
            if current in encountered:
                other_i, other_before_height = encountered[current]
                to_cover = 1000000000000 - other_i
                loop_size = i - other_i
                repeated = ((to_cover // loop_size) - 1) * (before_height - other_before_height)
                left_over_size = to_cover % loop_size
                left_over = self.simulate(before_grid, left_over_size, before_blow_index, i)
                return repeated + left_over
            encountered[current] = i, before_height
        return -min(y for _, y in grid) + 1

    def simulate(self, grid, iterations, blow_index=0, start=0):
        blows = self.parse_input()

        for i in range(start, iterations + start):
            shape = self.SHAPES[i % len(self.SHAPES)]
            shape = self.start_position(shape, grid)
            updated = True
            while updated:
                shape = self.blow(shape, blows[blow_index], grid)
                updated, shape = self.fall(shape, grid)
                blow_index = (blow_index + 1) % len(blows)
            grid = grid.union(shape)
        return -min(y for _, y in grid) + 1

    def get_shape(self, grid):
        highest = min(y for _, y in grid) if len(grid) > 0 else 1
        result = []
        for i in range(7):
            target = [y for x, y in grid if x == i]
            result.append(min(target) - highest if len(target) > 0 else 0)
        return tuple(result)


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