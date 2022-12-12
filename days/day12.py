import queue

from lib.day import Day


class Day12(Day):
    def part1(self):
        start, end, heights = self.parse_input()
        return self.find_route(start, end, heights)

    def part2(self):
        start, end, heights = self.parse_input()
        result = float('inf')

        for cursor, height in heights.items():
            if height == ord('a'):
                result = min(result, self.find_route(cursor, end, heights, result))
        return result

    def find_route(self, start, end, heights, max_depth=float('inf')):
        considering = set()
        to_visit = queue.Queue(len(heights))
        considering.add(start)
        to_visit.put((start, 0))
        while to_visit.qsize() > 0:
            (x, y), depth = to_visit.get()

            if depth >= max_depth:
                return float('inf')

            if (x, y) == end:
                return depth

            for (delta_x, delta_y) in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                cursor = x + delta_x, y + delta_y
                if cursor in heights and cursor not in considering \
                        and heights[cursor] - heights[(x, y)] <= 1:
                    considering.add(cursor)
                    to_visit.put((cursor, depth + 1))
        return float('inf')

    def parse_input(self):
        start = None
        end = None
        heights = dict()
        for y, line in enumerate(self.read_input().split()):
            for x, height in enumerate(line):
                if height == 'S':
                    start = (x, y)
                    heights[(x, y)] = ord('a')
                elif height == 'E':
                    end = (x, y)
                    heights[(x, y)] = ord('z')
                else:
                    heights[(x, y)] = ord(height)
        return start, end, heights
