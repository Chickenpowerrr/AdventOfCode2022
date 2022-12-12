import re
import time
from abc import abstractmethod, ABC
from functools import total_ordering


@total_ordering
class Day(ABC):
    def __init__(self):
        self._number = int(re.search('\\d+', self.__class__.__name__).group())

    def run(self):
        print('==============================================================')
        print(f'Running: {self.__class__.__name__}')

        start = time.perf_counter()
        result = self.part1()
        delta = time.perf_counter() - start

        print(f'Part 1: {str(result): <30} (took {delta:.5f} seconds)')

        start = time.perf_counter()
        result = self.part2()
        delta = time.perf_counter() - start

        print(f'Part 2: {str(result): <30} (took {delta:.5f} seconds)')

    def read_input(self) -> str:
        return open(f'resources/day{self._number:02}.txt').read()

    @abstractmethod
    def part1(self):
        pass

    @abstractmethod
    def part2(self):
        pass

    def get_number(self):
        return self._number

    def __eq__(self, other):
        return self._number == other._number

    def __lt__(self, other):
        return self._number < other._number
