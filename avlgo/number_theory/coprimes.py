from math import gcd
from collections import deque

from avlgo.number_theory.primes_factorization import prime_factors


# We can also implement that by iterating up to n and return numbers i which gcd(i, n) = 1 O(log(n)).
# Another way could be get prime factors and use the chinese reminder theorem over all combinations of primes coprimes.
def coprimes(n):
    """
    Get list of all positive integers up to n that are relatively prime to n.

    Time Complexity: O(n * log(log(log(n))))
    Space Complexity: O(n)

    :param n: number to calculate coprimes of
    :type n: int
    :return: {0<x<n| gcd(x, n) = 1}
    :rtype: list[int]
    """
    n_primes = [prime for prime, prime_exp in prime_factors(n)]
    is_coprime = [True] * n
    is_coprime[0] = False

    for n_prime in n_primes:
        for i in range(n_prime, n, n_prime):
            is_coprime[i] = False

    return [i for i, is_cp in enumerate(is_coprime) if is_cp]


def is_coprimes(a, b):
    """
    Check whether a, b are relatively prime.

    Time Complexity: O(log(n))
    Space Complexity: (O(1))

    :param a: first number
    :type: int
    :param b: second number
    :type b: int
    :rtype: bool
    """
    return gcd(a, b) == 1


def coprimes_generator(limit=float('inf')):
    """
    Generate all pairs of co-primes numbers up to a given limit

    Time Complexity: O(n^2) [There are ~nC2 * (6/pi^2) coprimes tuples up to n]
    Space Complexity: O(n^2)

    :param limit: maximal number to generate co-primes up to.
    :type limit: int
    :return: generator of co-primes number (a, b) where 0 < b < a < limit
    :rtype: list[tuple[int, int]]
    """
    coprimes_tree = deque([
        (2, 1),
        (3, 1)
    ])

    while coprimes_tree:
        a, b = coprimes_tree.popleft()
        yield a, b

        nodes = [
            (2 * a - b, a),
            (2 * a + b, a),
            (a + 2 * b, b)
        ]
        for node_a, node_b in nodes:
            if node_a < limit:
                coprimes_tree.append((node_a, node_b))


# Note that there are formulas for the sum of the 2/3/... pow of the coprimes in some articles.
# Because there is no clear formula for power p, I did not mention the formulas here.
# As we proved below, coprimes_sum(n) = n * Phi(n) / 2. So we can prove that it is almost multiplicative function.
# coprimes_sum(m * n) = (m * n) * Phi(m * n) / 2 =
# = (m * Phi(m) / 2) * (n * Phi(n) / 2) * 2 = 2 * coprimes_sum(m) * coprimes_sum(n)
# So basically, we could solve this problem with the same implementation as euler_totient, but there is no need.
def coprimes_sum(n):
    """
    Calculate the sum of all positive integers up to n that are relatively prime to n.

    Complexity Time: O(sqrt(n))
    Space Complexity: O(log(n))

    :param n: number to sum coprimes of
    :type n: int
    :return: SUM({0<x<n| gcd(x, n) = 1})
    :rtype: int
    """
    # coprime(k, n) iff coprime(n-k, n), therefore n coprimes can be divided to pairs which their's sum is n.
    # Because we have Phi(n) total numbers, coprimes_sum(n) = n * Phi(n) / 2
    return n * euler_totient(n) // 2


def coprimes_sum_range(limit):
    """
    Calculate the sum of positive integers up to i that are relatively prime to i for i in [1, limit].

    Time Complexity: O(n * log(log(n))
    Space Complexity: O(n)

    :param limit: limit to sum coprimes in range
    :type limit: int
    :return: coprimes_sum(i) for all i in [1, limit]
    :rtype: list[int]
    """
    return [i * phi_i // 2 for i, phi_i in enumerate(euler_totient_range(limit))]


def euler_totient(n):
    """
    Calculate Euler totient function (Phi).
    Number of positive integers up to n that are relatively prime to n.

    Complexity Time: O(sqrt(n))
    Space Complexity: O(log(n))

    :param n: number to calculate for
    :type n: int
    :return: LEN({0<x<n| gcd(x, n) = 1})
    :rtype: int
    """
    n_primes = [prime for prime, prime_exp in prime_factors(n)]

    phi_n = n
    for n_prime in n_primes:
        # Phi(m * n) = Phi(m) * Phi(n) if coprime(m, n)
        # Phi(p ^ k) = P ^ k * (1 - 1/p) for prime p
        # If the prime factorization of n = PI(Pi ^ Ai), then Phi(n) = n * PI(1 - 1/p)
        phi_n //= n_prime
        phi_n *= n_prime - 1

    return phi_n


def euler_totient_range(limit):
    """
    Calculate the euler totient function for all numbers in [0, limit]

    Time Complexity: O(n * log(log(n))
    Space Complexity: O(n)

    :param limit: number to calculate in range for
    :type limit: int
    :return: [Phi(i) for i in [0, limit]]
    :rtype: list[int]
    """
    phis = [i for i in range(limit + 1)]

    for prime in range(2, limit + 1):
        if prime != phis[prime]:
            # Prime test: no prime
            # if the i'th place has changed, i is a prime number.
            continue

        for i in range(prime, limit + 1, prime):
            # Phi(m * n) = Phi(m) * Phi(n) if coprime(m, n)
            # Phi(p ^ k) = P ^ k * (1 - 1/p) for prime p
            # If the prime factorization of n = PI(Pi ^ Ai), then Phi(n) = n * PI(1 - 1/p)
            phis[i] //= prime
            phis[i] *= prime - 1

    return phis
