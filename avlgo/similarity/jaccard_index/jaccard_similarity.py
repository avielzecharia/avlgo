

class JaccardSimilarity:
    """
    Jaccard index of sets A, b can be calculated by the size of sets intersections divided by their union size.

    This class describes a general API for Jaccard index similarity problem.
    The default implementation is the trivial solution for calculating J(A, B).

    Using the trivial technique:
    Sketch Storage Complexity: O(n * log(UNIVERSE))
    Similarity Time Complexity: O(n * log(UNIVERSE))
    """

    def __init__(self, genes_extractor):
        """
        :param genes_extractor: genes extractor logic from a given data
        :type genes_extractor: function
        """
        self._genes_extractor = genes_extractor

    def data_similarity(self, data1, data2):
        """
        Calculate the approximation of the Jaccard Index of data1 and data2.

        :return: Jaccard Index of data1, data2.
        :rtype: float
        """
        sketch1 = self.generate_sketch(data1)
        sketch2 = self.generate_sketch(data2)

        return self.jaccard_index(sketch1, sketch2)

    def generate_sketch(self, data):
        """
        Generate sketch for further comparison.

        :param data: data to generate sketch from
        :return: data sketch
        :rtype: set[int]
        """
        return set(self._genes_extractor(data))

    @staticmethod
    def jaccard_index(sketch1, sketch2):
        """
        Calculating the Jaccard Index of two given sketches.

        :type sketch1: set
        :type sketch2: set
        :return: Jaccard index J(S1, S2)
        :rtype: float
        """
        return len(sketch1.intersection(sketch2)) / len(sketch1.union(sketch2))
