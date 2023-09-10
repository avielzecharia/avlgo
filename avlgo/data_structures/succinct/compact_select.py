from collections import namedtuple
from math import log, floor


BlockData = namedtuple("BlockData", ["select_map", "size", "counter"])


class CompactSelect:
    """
    This class implements succinct compact data structure for the select query problem.
    Given an iterable of 0's & 1's, query index in which proceeds a given number of 1's.
    This data structure uses indirection technique, and can be improved to be succinct using 2 levels of indirection.
    Anyway, the improved implementation is not so relevant in practice and might be even more expansive.
    This implementation assuming the fact that python stores the ~minimal necessary number of bits for integers.

    Complexity: n = number of elements.
        Pre-Processing Time Complexity: O(n).
        Query Time Complexity:  O(1).
        Total Space Complexity: O(n * loglog(n)).
    """
    def __init__(self, elements):
        """
        Pre-Processing Select DS on elements.

        Time Complexity: O(n)
        Space Complexity: O(n * loglog(n))

        :param elements: elements to query on.
        :type elements: iterable with __getitem__, __len__
        """
        self._size = len(elements)
        self._block_size = max(floor(log(self._size, 2) ** 2), 1)
        self._counter = 0

        self._blocks_select_map = []
        self._blocks_offsets = [0]
        scanner = 0
        while scanner < self._size:
            block_data = self._process_next_block(elements, scanner, self._block_size)
            scanner += block_data.size

            self._counter += block_data.counter
            self._blocks_select_map.append(block_data.select_map)
            self._blocks_offsets.append(scanner)

    def select(self, counter):
        """
        Calculate the index in which proceeds a given number of ones.

        Time Complexity: O(1)
        Space Complexity: O(1)

        :param counter: number to query.
        :type counter: int
        :returns: index
        :rtype: int
        """
        if not 0 < counter <= self._counter:
            raise IndexError(f"Query counter {counter} ot of range {self._counter}")

        counter -= 1
        block_index = counter // self._block_size
        block_inner_index = counter % self._block_size
        block_select_map = self._blocks_select_map[block_index]

        return self._blocks_offsets[block_index] + block_select_map[block_inner_index]

    def __len__(self):
        return self._size

    @property
    def counter(self):
        return self._counter

    @staticmethod
    def _process_next_block(elements, index, expected_count):
        """
        Generating a block select mapping for the next count 1's bits.

        Time Complexity: O(block size)
        Space Complexity: O(expected_count)

        :type elements: iterable with __getitem__
        :type index: int
        :type expected_count: int
        :rtype: BlockData
        """
        counter = 0
        select_map = []

        element_scanner = index
        while element_scanner < len(elements) and counter < expected_count:
            element = bool(elements[element_scanner])
            if element:
                counter += element
                select_map.append(element_scanner - index)

            element_scanner += 1

        return BlockData(select_map, element_scanner - index, counter)
