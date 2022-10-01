from itertools import islice, accumulate
from math import log, floor


class CompactRank:
    """
    This class implements succinct compact data structure for the rank query problem.
    Given an iterable of 0's & 1's, query number of ones proceeds a given index.
    This data structure uses indirection technique, and can be improved to be succinct using 2 levels of indirection.

    Complexity: n = number of elements.
        Pre-Processing Time Complexity: O(n).
        Query Time Complexity:  O(1).
        Total Space Complexity: O(n).
    """
    def __init__(self, elements):
        """
        Initialize

        Time Complexity: O(n)
        Space Complexity: O(n)

        :param elements: elements to
        :type elements: iterable
        """
        self._size = len(elements)
        self._block_size = floor(log(self._size, 2) / 2)

        self._blocks = list(accumulate(
            sum(islice(elements, ind, ind + self._block_size))
            for ind in range(0, self._size, self._block_size)
        ))
        self._blocks.insert(0, 0)       # _blocks[x] is the sum of all 1's elements up to _block_size * x

        self._block_bruteforce = self._generate_bruteforce_map(self._block_size)

    def rank(self, index):
        """
        Calculate the number of ones proceeds a given index.

        Time Complexity: O(1)
        Space Complexity: O(1)

        :param index: index to query.
        :type index: int
        :rtype: int
        """
        if not 0 <= index <= self._size:
            raise IndexError(f"Query index {index} ot of range {self._size}")

        return self._blocks[index // self._block_size] + self._block_bruteforce[index % self._block_size]

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
