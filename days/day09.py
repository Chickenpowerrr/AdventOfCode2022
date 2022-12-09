from lib.day import Day


class Day09(Day):
    def part1(self):
        head = tail = (0, 0)
        visited = {tail}
        for line in self.read_input().split('\n'):
            direction, size = tuple(line.split())
            size = int(size)
            for _ in range(size):
                head = self.next_head(head, direction)
                tail = self.next_tail(head, tail)
                visited.add(tail)
        return len(visited)

    def part2(self):
        head = (0, 0)
        tails = [(0, 0) for _ in range(9)]
        visited = {head}
        for line in self.read_input().split('\n'):
            direction, size = tuple(line.split())
            size = int(size)
            for _ in range(size):
                head = self.next_head(head, direction)
                tails[0] = self.next_tail(head, tails[0])
                for i in range(1, len(tails)):
                    tails[i] = self.next_tail(tails[i - 1], tails[i])
                visited.add(tails[-1])
        return len(visited)

    def next_head(self, head, direction):
        if direction == 'U':
            return head[0], head[1] + 1
        elif direction == 'D':
            return head[0], head[1] - 1
        elif direction == 'L':
            return head[0] - 1, head[1]
        elif direction == 'R':
            return head[0] + 1, head[1]

    def next_tail(self, head, tail):
        potential_tail = tail[0] + self.delta_tail(head[0], tail[0]), \
                         tail[1] + self.delta_tail(head[1], tail[1])
        return potential_tail if head != potential_tail else tail

    def delta_tail(self, head: int, tail: int):
        if head > tail:
            return 1
        elif head < tail:
            return -1
        return 0
