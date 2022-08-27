from math import comb
import numpy as np

from avlgo.number_theory.fibonacci import fibonacci_nth
from avlgo.number_theory.primes import prime_nth
from avlgo.number_theory.utils import power
from avlgo.number_theory.progression_sums import consecutive_progression_sum


prime_nth = prime_nth
fibonacci_nth = fibonacci_nth


def triangular_nth(n):
    """
    Calculate the nth triangular number.

    Time Complexity: O(1)
    Space Complexity: O(1)

    :param n: index
    :type n: int
    :return: Tn
    :rtype: int
    """
    return consecutive_progression_sum(n)


def pentagonal_nth(n):
    """
    Get the nth Pentagonal number.

    Time Complexity: O(1)
    Space Complexity: O(1)

    :param n: index
    :type n: int
    :return: Pn
    :rtype: int
    """
    return n * (3 * n - 1) // 2


def catalan_nth(n):
    """
    Calculates the nth Catalan number.

    Catalan numbers as a lot of usages !
    e.g. number of paths below the diagonal, convex polygon triangular partitions, etc.

    Time Complexity: O(n)
    Space Complexity: O(1)

    :param n: index
    :type n: int
    :return: Cn
    :rtype: int
    """
    return comb(2 * n, n) // (n + 1)


def linear_recursive_sequence_nth(n, coefficients, base_cases, mod=None):
    """
    Calculate the nth element in a custom linear recursive series.

    S(n) = coefficients[0] * S(n-1) + ... + coefficients[k] * S(n-k-1)
    S(0) = base_cases[0], ... , S(k-1) = base_cases[k-1]

    Time Complexity: O((#coeff ^ 3) * log(n))
    Space Complexity: O(#coeff ^ 2)

    Note: there is a limitation of longlong while multiply matrix (since using numpy).

    :param n: nth element to get from the series.
    :type n: int
    :param coefficients: coefficients which defines rhe series
    :type coefficients: list
    :param base_cases: recursive base cases
    :type base_cases: list
    :param mod: calc S(n) % mod instead of S(n)
    :type mod: int
    :return: S(n)
    """
    # S(n+k) = sigma C(i) * S(n+k-i-1) for i in coefficients indexes.
    # ------------------------------------------------------------------------------------------
    # | S(n+k) |   |C(0) C(1) ... C(k-1) C(k)|   |S(n+k-1)|   |Coefficients|       |  B(k-1)  |
    # |S(n+k-1)|   | 1    0   ...   0     0  |   |S(n+k-2)|   |1 0 .... 0 0|       |   ....   |
    # |  ...   | = | 0    1   ...   0     0  | * |   ...  | = |0 1 .... 0 0| ^ n * |Base-Cases|
    # | S(n+1) |   |   ...    ...     ...    |   |  S(n)  |   |    ....    |       |   ....   |
    # |  S(n)  |   | 0    0   ...   1     0  |   | S(n-1) |   |0 0 .... 1 0|       |   B(0)   |
    # ------------------------------------------------------------------------------------------
    matrix_size = len(coefficients)
    if matrix_size != len(base_cases):
        raise ValueError("number of base_cases must be equal to number of coefficients !")

    base_vector = np.array(base_cases).reshape(matrix_size, 1)[::-1]
    transition_matrix = np.identity(matrix_size, 'longlong')
    transition_matrix = np.roll(transition_matrix, matrix_size)
    transition_matrix = np.matrix(transition_matrix)
    transition_matrix[0] = coefficients

    transition_matrix_pow = power(
        transition_matrix,
        n,
        identity=np.matrix(np.identity(matrix_size, 'longlong')),
        mod=mod
    )
    output_vector = transition_matrix_pow * base_vector
    if mod:
        output_vector %= mod

    return output_vector.tolist()[-1][0]    # Extract S(n)
