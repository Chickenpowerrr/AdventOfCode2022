from lib.day import Day


class Day20(Day):
    def part1(self):
        circular_list = self.parse_input()
        for i in range(len(circular_list)):
            circular_list.move(i)

        return circular_list.search_index(1000) \
               + circular_list.search_index(2000) \
               + circular_list.search_index(3000)

    def part2(self):
        pass

    def parse_input(self):
        original_list = list(map(int, self.read_input().split()))
        return CircularList(original_list)


class CircularList:
    def __init__(self, wrapping):
        self.head = Node(0, wrapping[0], None, None)
        self.original_indices = [self.head]
        self.zero = None

        previous = self.head
        for i, value in enumerate(wrapping[1:], 1):
            cursor = Node(i, value, previous, None)
            previous.next = cursor

            if value == 0:
                self.zero = cursor

            self.original_indices.append(cursor)
            previous = cursor

        self.tail = previous
        self.tail.next = self.head
        self.head.previous = self.tail
        self.length = len(wrapping)

    def __len__(self):
        return self.length

    def search_index(self, index):
        cursor = self.zero
        for _ in range(index % self.length):
            cursor = cursor.next
        return cursor.value

    def move(self, original_index):
        to_move = self.original_indices[original_index]

        next_position = to_move

        offset = to_move.value // self.length if to_move.value < 0 else 0

        for _ in range((to_move.value % self.length) + offset):
            next_position = next_position.next

        if to_move == next_position:
            return

        if to_move == self.head:
            self.head = to_move.next

        to_move.previous.next = to_move.next
        to_move.next.previous = to_move.previous

        to_move.next = next_position.next
        to_move.previous = next_position

        next_position.next.previous = to_move
        next_position.next = to_move

    def __str__(self):
        cursor = self.head
        result = [cursor.value]
        for _ in range(self.length - 1):
            cursor = cursor.next
            result.append(cursor.value)
        return result.__str__()


class Node:
    def __init__(self, original_index, value, previous, next):
        self.original_index = original_index
        self.value = value
        self.previous = previous
        self.next = next
