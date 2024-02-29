

def arithmetic_progression_sum(a1, an, n, mod=None):
    """
    Calculates the sum of Arithmetic Progression.

    Time Complexity: O(1)
    Space Complexity: O(1)

    :param a1: first element
    :type a1: float
    :param an: last element
    :type an: float
    :param n: number of elements
    :type n: int
    :param mod: calculates the sum modulo mod
    :type mod: int
    :return: series sum
    :rtype: float
    """
    result = (a1 + an) * n // 2
    if mod:
        result %= mod

    return result


def geometric_progression_sum(a1, q, n):
    """
    Calculates the sum of Geometric Progression.

    Time Complexity: O(1)
    Space Complexity: O(1)

    :param a1: first element
    :type a1: float
    :param q: sequence common ratio
    :type q: float
    :param n: number of elements
    :type n: int
    :return: series sum
    :rtype: float
    """
    # 1-q must divide 1-q^n, therefore we first divide for better performance
    return (1 - q ** n) // (1 - q) * a1


def geometric_progression_inf_sum(a1, q):
    """
    Calculates the sum of infinite Geometric Progression.

    Time Complexity: O(1)
    Space Complexity: O(1)

    :param a1: first element
    :type a1: float
    :param q: sequence common ratio (0 < q < 1)
    :type q: float
    :return: sum(a1 * q ^ i) for i in [1, INF]
    :rtype: float
    """
    # sum(q ^ i) for i in [1, INF] = (1-q)^-1 for 0 < q < 1
    return a1 / (1 - q)


def consecutive_progression_sum(end, p=1, start=1, mod=None):
    """
    Calculate the sum of the form start^p ... + end^p

    Time Complexity: O(1)
    Space Complexity: O(1)

    :param end: last elements
    :type end: int
    :param p: the power
    :type p: int
    :param start: first element to sum from
    :type start: int
    :param mod: calculates the result modulo mod
    :type mod: int
    :return: sigma(i ^ p) for i in [start, end]
    :rtype: int
    """
    if start > end:
        return 0
    if start != 1:
        result = consecutive_progression_sum(end, p) - consecutive_progression_sum(start - 1, p)
        return result % mod if mod else result

    if p == 0:
        return end % mod if mod else end
    if p == 1:
        return arithmetic_progression_sum(1, end, end, mod)
    if p == 2:
        result = end * (end + 1) * (2 * end + 1) // 6
        return result % mod if mod else result
    if p == 3:
        return pow(consecutive_progression_sum(end, 2), 2, mod)     # Nicomachus's theorem

    # TODO: implementation using Bernoulli Numbers
    raise NotImplementedError("Currently support powers {0,1,2,3} only ")
