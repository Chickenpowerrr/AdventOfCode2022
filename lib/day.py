import re
import time
from abc import abstractmethod, ABC


class Day(ABC):
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
        day = re.search('\\d+', self.__class__.__name__).group()
        return open(f'resources/day{day}.txt').read()

    @abstractmethod
    def part1(self):
        pass

    @abstractmethod
    def part2(self):
        pass
