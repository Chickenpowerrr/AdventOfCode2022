from lib.day import Day

DELTAS = (((0, -1), (1, -1), (-1, -1)),
          ((0, 1), (1, 1), (-1, 1)),
          ((-1, 0), (-1, -1), (-1, 1)),
          ((1, 0), (1, -1), (1, 1)))


class Day23(Day):
    def part1(self):
        elves = None
        next_elves = self.parse_input()
        delta_index = 0

        for i in range(11):
            elves = next_elves
            next_elves = {(x, y): self.next_position(x, y, elves, delta_index)
                          for x, y in elves}
            next_elves = set(self.remove_duplicates(next_elves).values())
            delta_index = (delta_index + 1) % len(DELTAS)
        return self.smallest_cube(elves) - len(elves)

    def part2(self):
        elves = None
        next_elves = self.parse_input()
        delta_index = 0

        result = 0
        while elves != next_elves:
            result += 1

            elves = next_elves
            next_elves = {(x, y): self.next_position(x, y, elves, delta_index)
                          for x, y in elves}
            next_elves = set(self.remove_duplicates(next_elves).values())
            delta_index = (delta_index + 1) % len(DELTAS)
        return result

    def smallest_cube(self, elves):
        min_x = min(x for x, _ in elves)
        max_x = max(x for x, _ in elves)
        min_y = min(y for _, y in elves)
        max_y = max(y for _, y in elves)

        return (max_x - min_x + 1) * (max_y - min_y + 1)

    def remove_duplicates(self, elves):
        duplicates = {position for position, count
                      in self.value_count(elves).items() if count > 1}
        result = {position: next_position if next_position not in duplicates else position
                  for position, next_position in elves.items()}
        return result

    def value_count(self, dictionary):
        count = dict()
        for _, value in dictionary.items():
            if value not in count:
                count[value] = 0
            count[value] += 1
        return count

    def next_position(self, x, y, elves, delta_index):
        if not self.has_neighbours(x, y, elves):
            return x, y

        for moves in DELTAS[delta_index:] + DELTAS[:delta_index]:
            possible = True
            for dx, dy in moves:
                if (x + dx, y + dy) in elves:
                    possible = False
            if possible:
                dx, dy = moves[0]
                return x + dx, y + dy
        return x, y

    def has_neighbours(self, x, y, elves):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                if (x + dx, y + dy) in elves:
                    return True
        return False

    def parse_input(self):
        elves = set()
        for y, line in enumerate(self.read_input().split()):
            for x, character in enumerate(line):
                if character == '#':
                    elves.add((x, y))
        return elves
