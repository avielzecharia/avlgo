from math import comb

from avlgo.number_theory.sequence_nth import linear_recursive_sequence_nth


# Another approach would be using the linear_equation_sol_counter, but this one is faster.
# in this function we are using one of the euler formula's for calculating p(n), there are much more cool formulas !
def integer_partition_range(n, mod=None):
    """
    Calculating the number of ways of writing all numbers from `start` to n as a sum of positive integers.
    Time Complexity: O(n ^ 1.5)
    Space Complexity: O(n)
    :type n: int
    :type mod: int
    :return: list of number of partitions for all number up to n.
    :rtype: list[int]
    """
    partitions = [1] + [0] * n

    for num in range(1, n + 1):
        # Euler's formula !
        # P(n) = sigma((-1) ^ (k+1) * P(n - k*(3*k-1)/2)) for non-zero k
        # Calculating positive k's
        i = 1
        pentagonal = 1
        while pentagonal <= num:
            partitions[num] += (i % 2 * 2 - 1) * partitions[num - pentagonal]
            pentagonal += 3 * i + 1
            i += 1
            if mod:
                partitions[num] %= mod

        # Calculating negative k's
        i = 1
        pentagonal = 2
        while pentagonal <= num:
            partitions[num] += (i % 2 * 2 - 1) * partitions[num - pentagonal]
            pentagonal += 3 * i + 2
            i += 1
            if mod:
                partitions[num] %= mod

    return partitions


def integer_partition(n, mod=None):
    """
    Calculating the number of ways of writing n as a sum of positive integers.
    Time Complexity: O(n ^ 1.5)
    Space Complexity: O(n)
    :type n: int
    :type mod: int
    :return: number of integer partitions of n.
    :rtype: int
    """
    return integer_partition_range(n, mod=mod)[-1]


def integer_k_composition(n, k):
    """
    Calculating the number of compositions of n into exactly k parts (a k-composition)
    Time Complexity: O(n)
    Space Complexity: O(1)
    :type n: int
    :type k: int
    :return: number of k-compositions of n.
    :rtype: int
    """
    # In order to calculate the k-composition of n, let's examine the following pattern:
    # 1 _ 1 _ 1 _ 1 ... 1 _ 1 (n times 1)
    # where we can choose to put ',' or '+' in each _ in order to produce unique composition.
    # But, we want to have only k-1 ',' in order to produce k numbers.
    # Therefore we got (n-1)C(k-1) options :)
    # Stars and bars theorem 1 !
    return comb(n-1, k-1)


def integer_weak_k_composition(n, k):
    """
    Calculating the number of compositions of n into exactly k parts (a k-composition) allowing zeros.
    Time Complexity: O(n)
    Space Complexity: O(1)
    :type n: int
    :type k: int
    :return: number of weak k-compositions of n.
    :rtype: int
    """
    # In order to calculate the weak k-composition of n, let's examine the following pattern:
    # 1 _ 1 _ 1 _ 1 ... 1 _ 1 (n times 1)
    # where we can choose to put multiple ',' or '+' in each _ in order to produce unique composition.
    # But, we want to have only k-1 ',' in order to produce k numbers where we can choose to put more than 1 ','.
    # Therefore we got (n+k-1)C(k-1) options :)
    # Stars and bars theorem 2 !
    return comb(n+k-1, k-1)


def integer_compositions(n, mod=None):
    """
    Calculates the number of integer partitions with order matter - integer composition.
    Time Complexity: O(log(n))
    Space Complexity: O(1)
    :type n: int
    :type mod: int
    :return: number of ways to write n as a sum of number with order matter.
    :rtype: int
    """
    # In order to find n compositions, let's examine the following pattern:
    # 1 _ 1 _ 1 _ 1 ... 1 _ 1 (n times 1)
    # where we can choose to put ',' or '+' in each _ in order to produce unique composition.
    # Therefore, we got 2 ^ (n-1) choices [we got n-1 empty _]
    # We can only prove that by sigma(k-composition(n)) k=1 to n = sigma(nCk) k=0 to n-1 = 2 ^ (n-1)
    # Stars and bars theorem 1 !
    if n == 0:
        return 1

    return pow(2, n-1, mod)


def integer_composition_forcing_k_range(n, k, mod=None):
    """
    Calculates number of integer composition which contains the integer k for all numbers up to n.
    Time Complexity: O(n)
    Space Complexity: O(n)
    :type n: int
    :type k: int
    :type mod: int
    :return: all compositions of 1...n which must contain k.
    :rtype: list[int]
    """
    # In order to solve that problem, we will use generating functions tools.
    # Note that we are already know that the number of integer compositions is 2 ^ (n-1).
    # Let Ci(Z) be the generating function of the number of integer compositions *not* contains k.
    # Ci(Z) = [(Z + Z^2 + Z^3 + ...) - Z^k] ^ i = [Z / (1 - Z) - Z^k] ^ i
    # Then, our final generating function would be
    # C(Z) = sigma (Ci(Z)) i=0 to INF = 1 / (1 - C1(Z)) = ... = (1 - z) / (1 - 2z + z^k - z^(k+1))
    # So our result f(n) can be expressed recursively by the denominator:
    # f(n) = 2f(n-1) - f(n-k) + f(n-k-1). f(l) = 2 ^ (l-1) [l<k], f(k) = 2 ^ (k-1) - 1, f(k+1) = 2 ^ k - 2.
    # So, we are interested in the function
    # g(n) = 2 ^ (n-1) - f(n) = ... = 2g(n-1) - g(n-k) + g(n-k-1) + 2 ^ (n-k-2)

    # Base cases
    composition_k = [0] * (n + 1)
    composition_k[k] = 1
    composition_k[k+1] = 2 if k != 1 else 1
    if mod:
        composition_k[k] %= mod
        composition_k[k+1] %= mod

    pow_2 = 1
    for num in range(k+2, n+1):
        composition_k[num] = 2 * composition_k[num-1] - composition_k[num-k] + composition_k[num-k-1] + pow_2
        pow_2 *= 2
        if mod:
            composition_k[num] %= mod
            pow_2 %= mod

    return composition_k


def integer_composition_forcing_non_k(n, k, mod=None):
    """
    Calculates number of integer composition which must not contain the integer k.
    Note: for large k's, please use the range method.
    Time Complexity: O(k ^ 3 * log(n))
    Space Complexity: O(k ^ 2)
    :type n: int
    :type k: int
    :type mod: int
    :return: number of compositions of n without k.
    :rtype: int
    """
    base_cases = [0] * (k + 2)
    base_cases[k] = 1
    base_cases[k + 1] = 2 if k != 1 else 1

    pow_2 = 1
    for i in range(1, k+2):
        base_cases[i] = pow_2 - base_cases[i]
        pow_2 *= 2

    coefficients = [0] * (k + 2)
    coefficients[0] = 2
    coefficients[k - 1] = -1 if k != 1 else 1
    coefficients[k] = 1

    return linear_recursive_sequence_nth(
        n,
        coefficients,
        base_cases,
        mod=mod
    )


def integer_composition_forcing_k(n, k, mod=None):
    """
    Calculates number of integer composition which contains the integer k.
    Note: for large k's, please use the range method.
    Time Complexity: O(k ^ 3 * log(n))
    Space Complexity: O(k ^ 2)
    :type n: int
    :type k: int
    :type mod: int
    :return: number of compositions of n with k.
    :rtype: int
    """
    if n == 0:
        return 0

    result = integer_composition_forcing_non_k(n, k, mod=mod)
    result = pow(2, n-1, mod) - result
    if mod:
        result %= mod

    return result
