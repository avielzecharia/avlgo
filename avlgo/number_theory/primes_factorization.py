from collections import namedtuple
from math import sqrt

from avlgo.number_theory.primes import sieve_of_eratosthenes
from avlgo.number_theory.utils import omit_factor


PrimeFactor = namedtuple("PrimeFactor", ["base", "exp"])


def prime_exp(n, prime):
    """
    Calculate the power of p in the prime factorization of n.

    Time Complexity: O(log(n) / log(prime))
    Space Complexity: O(1)

    :type n: int
    :type prime: int
    :return: {max(e)| prime^e|n}
    :rtype: int
    """
    rest_part, p_exp = omit_factor(n, prime)
    return p_exp


def factorial_prime_exp(n, prime):
    """
    Calculating the power of p in the prime factorization of n! using legendre formula.
    Note that the result will be always be smaller or equal to (n - 1) / (p - 1).

    Time Complexity: O(log(n))
    Space Complexity: O(1)

    :type n: int
    :type prime: int
    :return: {max(e)| prime^e|n!}
    :rtype: int
    """
    fac_prime_exp = 0
    prime_mul = prime
    while prime_mul <= n:
        fac_prime_exp += n // prime_mul
        prime_mul *= prime

    return fac_prime_exp


def ncr_prime_exp(n, r, prime):
    """
    Calculating the power of p in the prime factorization of nCr using legendre formula.

    Time Complexity: O(log(n))
    Space Complexity: O(1)

    :type n: int
    :type r: int
    :type prime: int
    :return: {max(e)| prime^e|nCr}
    :rtype: int
    """
    return factorial_prime_exp(n, prime) - factorial_prime_exp(r, prime) - factorial_prime_exp(n - r, prime)


# TODO: Pollard’s Rho Algorithm ?
def prime_factors(n):
    """
    Calculates the primes factorization of n.

    Time Complexity: O(sqrt(n))
    Space Complexity: O(log(n))

    :param n: number to calculate prime factors of
    :type n: int
    :return: [PrimeFactor(p, p_exp), ...]
    :rtype: list[PrimeFactor]
    """
    prime_factor = 2
    factors = []
    n_sqrt = int(sqrt(n))

    while prime_factor <= n_sqrt:
        if n % prime_factor == 0:
            # We surely got a prime now, because it's the smallest number which divides n !
            n, p_exp = omit_factor(n, prime_factor)
            factors.append(PrimeFactor(prime_factor, p_exp))

        prime_factor += 1

    if n > 1:
        # For number n, there is might be only single prime p above sqrt(n) which divides him. (otherwise p * p > n)
        factors.append(PrimeFactor(n, 1))

    # In the worst case, n = 2 * 3 * 5 * 7 * ... * Pk which provides the maximal #factors k for a given n.
    # By number-theory, such n ~ e ^ Pk ~ e ^ (k * ln(k)) ~ k ^ k
    # So maximal #factors would be k for n = k ^ k
    # Solving that using Lambert W function, we get k = e ^ (W(ln(n)))
    # n -> INF, W(x) ~ O(ln(x)). therefore k ~ ln(n), so #factors ~ O(ln(n)) top.
    return factors


def prime_factors_range(n, primes=None):
    """
    Calculates the primes factorization for all number up to n.

    Time Complexity: O(n * log(log(n)))
    Space Complexity: O(n * log(log(n)))

    :param n: limit to calculate prime factors up to.
    :type n: int
    :param primes: list of primes up to n (pre-processed).
    :type primes: list[int]
    :return: [[PrimeFactor(p, p_exp), ...], [PrimeFactor(p, p_exp), ...], ...]
    :rtype: list[list[PrimeFactor]]
    """
    prime_factors_r = [[] for _ in range(n + 1)]
    primes = primes if primes else sieve_of_eratosthenes(n)

    # By Legendre theorem, each prime appears (n - 1) / (p - 1) times top.
    # As a result, we are counting & saving the prime power in the factorization at most (n - 1) / (p - 1)
    # time for all primes in [1, n], so the complexities are n * log(log(n)) [inverse primes sum]
    for prime in primes:
        for i in range(prime, n + 1, prime):
            prime_factors_r[i].append(PrimeFactor(prime, prime_exp(i, prime)))

    return prime_factors_r


def distinct_prime_factors_range(n, primes=None):
    """
    Calculates the distinct primes factorization for all number up to n.

    Time Complexity: O(n * log(log(n)))
    Space Complexity: O(n * log(log(n)))

    :param n: limit to calculate distinct prime factors up to.
    :type n: int
    :param primes: list of primes up to n (pre-processed).
    :type primes: list[int]
    :return: [[p1, ...], [p2, ...], ...]
    :rtype: list[list[int]]
    """
    distinct_prime_factors_r = [[] for _ in range(n + 1)]
    primes = primes if primes else sieve_of_eratosthenes(n)

    # By Legendre theorem, each prime appears (n - 1) / (p - 1) times top.
    # As a result, we are counting & saving the prime power in the factorization at most (n - 1) / (p - 1)
    # time for all primes in [1, n], so the complexities are n * log(log(n)) [inverse primes sum]
    for prime in primes:
        for i in range(prime, n + 1, prime):
            distinct_prime_factors_r[i].append(prime)

    return distinct_prime_factors_r


def factorial_prime_factors(n, primes=None):
    """
    Calculates the primes factorization of n! .

    Time Complexity: about O(n)
    Space Complexity: O(n)

    :type n: int
    :param primes: list of primes up to n (pre-processed).
    :type primes: list[int]
    :return: [PrimeFactor(p, p_exp), ...]
    :rtype: list[PrimeFactor]
    """
    primes = primes if primes else sieve_of_eratosthenes(n)

    return [
        PrimeFactor(prime, factorial_prime_exp(n, prime))
        for prime in primes
    ]


def ncr_prime_factors(n, r, primes=None):
    """
    Calculates the primes factorization of nCr.

    Time Complexity: about O(n)
    Space Complexity: O(n)

    :type n: int
    :type r: int
    :param primes: list of primes up to n (pre-processed).
    :type primes: list[int]
    :return: [PrimeFactor(p, p_exp), ...]
    :rtype: list[PrimeFactor]
    """
    primes = primes if primes else sieve_of_eratosthenes(n)

    factors = []
    for prime in primes:
        p_exp = ncr_prime_exp(n, r, prime)
        if p_exp:
            factors.append(PrimeFactor(prime, p_exp))

    return factors


def triangular_prime_factors(n):
    """
    Calculates the primes factorization of Tn.

    Time Complexity: O(sqrt(n))
    Space Complexity: O(log(n))

    :param n: triangular index
    :type n: int
    :return: [PrimeFactor(p, p_exp), ...]
    :rtype: list[PrimeFactor]
    """
    if n % 2:
        unsorted_primes = prime_factors(n) + prime_factors((n + 1) // 2)
    else:
        unsorted_primes = prime_factors(n // 2) + prime_factors(n + 1)

    return sorted(unsorted_primes)
