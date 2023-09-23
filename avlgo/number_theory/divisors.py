from math import log, sqrt

from avlgo.number_theory.primes import sieve_of_eratosthenes
from avlgo.number_theory.progression_sums import consecutive_progression_sum


def divisors(n):
    """
    Generate all divisors of a given number.

    Time Complexity: O(sqrt(n))
    Space Complexity: O(sqrt(n))

    :param n: number to generate divisors.
    :type n: int
    :return: sorted divisors list
    :rtype: list[int]
    """
    scanner = 1
    sqrt_up_divisors = []
    sqrt_down_divisors = []

    while scanner ** 2 < n:
        if n % scanner == 0:
            sqrt_down_divisors.append(scanner)
            sqrt_up_divisors.insert(0, n // scanner)
        scanner += 1

    if scanner ** 2 == n:
        sqrt_down_divisors.append(scanner)

    return sqrt_down_divisors + sqrt_up_divisors


# Another approach could be using prime factorization of n, and the fact that D_S is multiplicative function.
# Assuming n = PI(Pi ^ Ai) for i in [1, r], D_S = {sigma{Pi^j}} = PI{(Pi^(Ai + 1) - 1) / (Pi^x - 1)} for i in [1, r]
# But, calculating modulo in this approach would be inefficient for big numbers.
def divisors_sum(n, p=1, mod=None):
    """
    Calculates the divisor function (small sigma).

    Time Complexity: O(sqrt(n))
    Space Complexity: O(1)

    :param n: calculate sum of divisors of n
    :type n: int
    :param p: power the divisor before summing it
    :type p: int
    :param mod: return the result modulo mod
    :type mod: int
    :return: SUM({d^p| d|n}) % mod
    """
    divisor = 1
    d_sum = 0

    while divisor ** 2 < n:
        if n % divisor == 0:
            d_sum += pow(divisor, p, mod)
            d_sum += pow(n // divisor, p, mod)
            if mod:
                d_sum %= mod
        divisor += 1

    if divisor ** 2 == n:
        d_sum += divisor
        if mod:
            d_sum %= mod

    return d_sum


def divisors_sum_range(n, p=1, mod=None):
    """
    Calculates the divisors sum for all numbers in [1, n].

    Time Complexity: O(n * log(n))
    Space Complexity: O(n)

    :param n: limit to calculate the divisors sum to
    :type n: int
    :param p: power the divisor before summing it
    :type p: int
    :param mod: return the result modulo mod
    :type mod: int
    :return: [divisors_sum(i) for i in [1,n]]
    :rtype: list[int]
    """
    divisor = 1
    divisors_sums = [0] * (n + 1)

    while divisor <= n:
        for divided in range(divisor, n + 1, divisor):
            divisors_sums[divided] += pow(divisor, p, mod)
            if mod:
                divisors_sums[divided] %= mod

        divisor += 1

    return divisors_sums


def divisors_sum_range_sum(n, p=1, mod=None):
    """
    Calculates the sum of divisors sum for all numbers in [1, n].

    Time Complexity: O(sqrt(n))
    Space Complexity: O(sqrt(n))

    :param n: limit to calculate the divisors sum to
    :type n: int
    :param p: power the divisor before summing it
    :type p: int
    :param mod: return the result modulo mod
    :type mod: int
    :return: SUM{divisors_sum(i, p) for i in [1,n]} % mod
    :rtype: int
    """
    d_sum_range_sum = 0
    n_sqrt = int(sqrt(n))

    # sigma{divisors_sum_range(i)} for i in [1, n]
    # Take a look at divisors_sum_range, instead of marking number which divided by d, we may just sum them.
    # So, our result is sigma{(n // d) * d ^ p} for i in [1, n]
    # Now, we can use the trick that n // d resulting only ~ 2*sqrt(n) different values !
    # 1 <= d <= n // sqrt(n)  -  calculates sigma{(n // d) * d ^ p}
    for d in range(1, n // n_sqrt + 1):
        d_sum_range_sum += (n // d) * pow(d, p, mod)
        if mod:
            d_sum_range_sum %= mod

    # n // sqrt(n) < d <= n  -  distinct results of (n // d) are [1, sqrt(n) - 1]
    # So, the sum is sigma{d * sigma{(n // (d + 1)) ^ p to (n // d) ^ p}} for d in [1, sqrt(n) - 1]
    for d in range(1, n_sqrt):
        d_sum_range_sum += d * consecutive_progression_sum(n // d, p, start=n//(d+1)+1)
        if mod:
            d_sum_range_sum %= mod

    return d_sum_range_sum


def minimal_range_divisor(n, mod=None):
    """
    Calculates the minimal number which divided by all numbers from 1 to n.

    Time Complexity: O(n)
    Space Complexity: O(n)

    :param n: limit number to divide all numbers below
    :type n: int
    :param mod: calculates the result modulo mod
    :type mod: int
    :return: {min(x)| i|x for i=1 to n} % mod
    :rtype: int
    """
    # Our answer is basically LCM(1, 2, ..., n) which it costs O(n*log(n)) time to calculate naively.
    # First observation, any prime in the range [1, n] will be part of the result.
    # Second observation, given a prime - it's enough to consider the maximum power below n.
    min_div = 1
    primes = sieve_of_eratosthenes(n)

    for prime in primes:
        prime_pow = int(log(n, prime))
        min_div *= pow(prime, prime_pow, mod)
        if mod:
            min_div %= mod

    return min_div
