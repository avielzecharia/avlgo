from math import log, floor


class CompactRank:
    """
    This class implements succinct compact data structure for the rank query problem.
    Given an iterable of 0's & 1's, query number of 1's proceeds a given index.
    This data structure uses indirection technique, and can be improved to be succinct using 2 levels of indirection.

    Complexity: n = number of elements.
        Pre-Processing Time Complexity: O(n).
        Query Time Complexity:  O(1).
        Total Space Complexity: O(n).
    """
    def __init__(self, elements):
        """
        Pre-Processing Rank DS on elements.

        Time Complexity: O(n)
        Space Complexity: O(n)

        :param elements: elements to query on.
        :type elements: iterable with __getitem__, __len__
        """
        self._size = len(elements)
        self._block_size = max(floor(log(self._size, 2) / 2), 1)
        self._block_bruteforce = self._generate_bruteforce_map(self._block_size)

        ones_counter = 0
        self._blocks_counter = [0]          # number of 1's up to a given block
        self._blocks_integer = []           # integer representation of a given block
        for block_start in range(0, self._size, self._block_size):
            block_end = min(block_start + self._block_size, self._size)

            block_integer = 0
            for element_ind in range(block_start, block_end):
                element = bool(elements[element_ind])
                ones_counter += element
                block_integer = 2 * block_integer + element

            self._blocks_counter.append(ones_counter)
            self._blocks_integer.append(block_integer)

    def rank(self, index):
        """
        Calculate the number of ones proceeds a given index.

        Time Complexity: O(1)
        Space Complexity: O(1)

        :param index: index to query.
        :type index: int
        :returns: counter
        :rtype: int
        """
        if not 0 <= index < self._size:
            raise IndexError(f"Query index {index} out of range 0...{self._size}")

        block_index = index // self._block_size
        block_inner_index = index % self._block_size

        block_start = block_index * self._block_size
        block_end = min(block_start + self._block_size, self._size)
        real_block_size = block_end - block_start

        block_inner_integer = self._blocks_integer[block_index] >> (real_block_size - block_inner_index)
        return self._blocks_counter[block_index] + self._block_bruteforce[block_inner_integer]

    def __len__(self):
        return self._size

    @staticmethod
    def _generate_bruteforce_map(size):
        """
        Generating a bruteforce 1's counting map for #size bits range.

        Time Complexity: O(n*log(n))
        Space Complexity: O(2^n)

        :type size: int
        :rtype: list[int]
        """
        map_size = pow(2, size)
        result = [0] * map_size

        scanner = 1
        while scanner < map_size:
            # given a power of 2 (scanner), count the numbers which contains it in the binary representation.
            for chunk in range(scanner, map_size, 2 * scanner):
                for i in range(scanner):
                    result[chunk + i] += 1

            scanner *= 2

        return result
