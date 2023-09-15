import heapq
import math
import statistics

from avlgo.similarity.jaccard_index.jaccard_similarity import JaccardSimilarity


class JaccardMinHash(JaccardSimilarity):
    """
    This class implements the approximation version of the Jaccard Index Similarity algorithm.

    NOTE: This implementation uses a single hash function technique.

    Using the MinHash technique:
    Sketch Time Complexity: O((genes + 1/e^2) * log(1/d))
    Sketch Storage Complexity: O(1/e^2 * log(1/d) * log(HASH_UNIVERSE))
    Similarity Time Complexity: O(1/e^2 * log(1/d))
    """
    def __init__(self, genes_extractor, approximation_rate, approximation_probability, hash_func=hash):
        """
        :param genes_extractor: genes extractor logic from a given data
        :type genes_extractor: function
        :param approximation_rate: promised multiplicative approximation bounds (known as epsilon).
        :type approximation_rate: float
        :param approximation_probability: probability that the promised approximation will be in bound (known as delta).
        :type approximation_probability: float
        :param hash_func: universal hash function for genes ordering. The function signature must be:
                            def sim_hash(data, seed=?): return int
        :type hash_func: function obj, int -> int
        """
        super().__init__(genes_extractor)
        self._genes_extractor = genes_extractor
        self._approximation_rate = approximation_rate
        self._approximation_probability = approximation_probability
        self._hash_genes_func = hash_func

        self._block_max_sketch_size = math.ceil(1 / self._approximation_rate ** 2)
        self._block_sketch_repeat = math.ceil(math.log(1 / self._approximation_probability))

    def generate_sketch(self, data):
        """
        Generate sketch for further comparison.

        :param data: data to generate sketch from
        :return: data sketch
        :rtype: list[set[int]]
        """
        genes = set(self._genes_extractor(data))
        block_sketch_size = min(len(genes), self._block_max_sketch_size)

        return [
            set(heapq.nsmallest(
                n=block_sketch_size,
                iterable=[self._hash_genes_func(gene, seed) for gene in genes]
            ))
            for seed in range(self._block_sketch_repeat)
        ]

    def jaccard_index(self, sketch1, sketch2):
        """
        Calculating the approximated Jaccard Index of two given sketches.

        :type sketch1: list[set[int]]
        :type sketch2: list[set[int]]
        :return: Jaccard index J(S1, S2)
        :rtype: float
        """
        return statistics.median(
            len(block_sketch1.intersection(block_sketch2)) / len(block_sketch1.union(block_sketch2))
            for block_sketch1, block_sketch2 in zip(sketch1, sketch2)
        )

    @property
    def approximation_probability(self):
        """
        Get the probability that the promised approximation will be in bound (known as delta).

        :return: delta
        :rtype: float
        """
        return self._approximation_probability

    @property
    def approximation_rate(self):
        """
        Get the promised multiplicative approximation bounds (known as delta).

        :return: epsilon
        :rtype: float
        """
        return self._approximation_rate

    @property
    def sketch_max_size(self):
        """
        Calculate the desired output sketch size.

        NOTE: Sketch size might be smaller, in case the input genes are too small.

        :rtype: int
        """
        return self._block_max_sketch_size * self._block_sketch_repeat
