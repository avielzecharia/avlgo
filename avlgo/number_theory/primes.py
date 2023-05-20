from math import sqrt, ceil, floor, log
from random import randrange

from avlgo.number_theory.progression_sums import consecutive_progression_sum
from avlgo.number_theory.utils import omit_factor


# There are much more sieves such as wheel-sieves, sieve of Sundaram.
# We could use Wilson's theorem to calculate all primes up to n in O(n), but we should save really large numbers...
def sieve_of_eratosthenes(limit):
    """
    Get all primes up to limit using Eratosthenes sieve.

    Time Complexity: O(n * log(log(n))) {Sigma(n/p) for prime p in [1,sqrt(n)}
    Space Complexity: O(n)

    :param limit: the upper limit to calculate all primes to.
    :type limit: int
    :return: list of all primes in range [1, limit]
    :rtype: list[int]
    """
    if limit < 2:
        return []

    size = (limit + 1) // 2
    primes_indicator = [True] * size   # is_primes[i] iff 2i+1 is prime [primes are odd, except 2]
    primes_indicator[0] = False
    limit_sqrt = int(sqrt(limit)) // 2 + 1

    for p in range(1, limit_sqrt):
        # It is enough to do sieve with the first sqrt primes p.
        # All number above sqrt(n) and below n will never contains only primes above sqrt(n)...
        # So, they will be marked as non-prime by the prime which is smaller then sqrt(n)
        if not primes_indicator[p]:
            continue

        for mul in range(2 * p * (p + 1), size, 2 * p + 1):
            # Iterating over the current prime q=2p+1
            # Normally, we would iterate over range(q * q, size, 2 * q)
            # {q*q and not 2*q because all the previous multiplies of q was already marked as composite by prev primes}
            # {2 * q and not q because q * q in order to avoid even numbers (q * q is odd)}
            # Now, we would like to iterate over it where q=2p+1, and then normalize it to "p" language
            # So, q * q // 2 == 2 * p * (p + 1) and 2 * q // 2 == 2 * p + 1
            primes_indicator[mul] = False

    primes = [
        2 * p + 1
        for p, is_p in enumerate(primes_indicator) if is_p
    ]
    primes.insert(0, 2)
    return primes


def sieve_of_atkin(limit):
    """
    Generate all primes up to limit using Atkin sieve.

    Time Complexity: O(n)
    Space Complexity: O(n)

    :param limit: the upper limit to calculate all primes to.
    :type limit: int
    :return: list of all primes in range [1, limit]
    :rtype: list[int]
    """
    if limit < 2:
        return []
    if limit == 2:
        return [2]

    primes_indicator = [False] * (limit + 1)
    limit_sqrt = ceil(sqrt(limit))

    for x in range(limit_sqrt):
        x_square = x ** 2
        for y in range(limit_sqrt):
            y_square = y ** 2
            # All numbers n which n % 60 is {1, 13, 17, 29, 37, 41, 49, 53} are primes if and only if
            # the number of solutions to `4 * x^2 + y^2 = n` where x, y in [1, n] is odd and the number is square-free !
            n = 4 * x_square + y_square
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                primes_indicator[n] = not primes_indicator[n]

            # All numbers n which n % 60 is {7, 19, 31, 43} are primes if and only if
            # the number of solutions to `3 * x^2 + y^2 = n` where x, y in [1, n] is odd and the number is square-free !
            n = 3 * x_square + y_square
            if n <= limit and n % 12 == 7:
                primes_indicator[n] = not primes_indicator[n]

            # All numbers n which n % 60 is {11, 23, 47, 59} are primes if and only if
            # the number of solutions to `3 * x^2 - y^2 = n` where x, y in [1, n] is odd and the number is square-free !
            n = 3 * x_square - y_square
            if n <= limit and x > y and n % 12 == 11:
                primes_indicator[n] = not primes_indicator[n]

    # Fot this point, primes_indicator at index i is:
    # False, then the i is not prime for sure.
    # True, then i is prime if and only if i is square-free.
    for prime in range(5, limit_sqrt):
        if primes_indicator[prime]:
            for non_square_free in range(prime ** 2, limit, prime ** 2):
                primes_indicator[non_square_free] = False

    primes = [
        prime for prime, is_p in enumerate(primes_indicator)
        if is_p and prime > 4
    ]
    primes.insert(0, 3)
    primes.insert(0, 2)
    return primes


# This method is very useful, because if we asked to calculate some sum which related to primes we can use that.
# e.g. sum factorizations of a factorial S(5) = 2+2+2+3+5
# Calculating primes below sqrt n will be easy, using Legendre's formula.
# All primes from N // 2 to N // 1 appears exactly once, so we can calc 1 * sum in this range
# All primes from N // 3 to N // 2 appears exactly twice, so we can calc 2 * sum in this range
# ...
# All primes from N // sqrt(n) to N // (sqrt(n) - 1) appears exactly sqrt(n) - 1 times, ...
def prime_sum_in_sqrt_ranges(limit):
    """
    Get all primes sum up the following ranges: [1, 2, ..., sqrt(n)] [n, n // 2, ..., n // (sqrt(n)-1), n // (sqrt(n))]

    Time Complexity: O(n ^ 0.75 / log(n))
    Space Complexity: O(sqrt(n))

    :param limit: upper limit for primes sum.
    :type limit: int
    :return: 2 lists sqrt_down, sqrt_up with size sqrt(n)
             sqrt_down[i] gives the sum of primes up to i
             sqrt_up[i] gives the sum of primes up to n // i
    :rtype: tuple[list[int], list[int]]
    """
    # TODO: make is sum with pow (maybe also mod)
    if limit <= 1:
        raise ValueError("{} too small".format(limit))

    limit_sqrt = int(sqrt(limit))

    # Initialize output lists with sum of all numbers from 2 up to i (or n // i)
    # 1 is excluded in order to avoid subtraction of the current prime in the progress later.
    sqrt_down = [int(consecutive_progression_sum(n, start=2)) for n in range(limit_sqrt + 1)]
    sqrt_up = [0] + [int(consecutive_progression_sum(limit // i, start=2)) for i in range(1, limit_sqrt + 1)]

    for prime in range(2, limit_sqrt + 1):
        # Now, for each iteration update the ith place in the arrays to be the sum of all
        # numbers up to i (or n // i), except number which divides by already seen primes. [basically, a sieve]
        if sqrt_down[prime - 1] == sqrt_down[prime]:
            # is not prime
            continue

        known_primes_sum = sqrt_down[prime - 1]
        prime_square = prime ** 2
        elements_to_update = min(limit_sqrt, limit // prime_square) + 1

        # Updating the sqrt_up
        for i in range(1, elements_to_update):
            # Basically, we may iterate on the first sqrt(n) elements and update their's sum.
            # But, we may also note the indexes in the range(n // prime_square, sqrt(n)) would not be updated anymore !
            # Why ? because at this point sqrt_up does not contain the sum of numbers which divided by the primes
            # that are smaller than p, all the numbers below p * p are such numbers.
            # Therefore, in sqrt_up all the indexes above n // prime_square but below sqrt(n) are such numbers :)
            d = i * prime
            if d <= limit_sqrt:
                # Reduce all the multiplies of the current prime from the ith sum,
                # while keeping the sum of the primes by the known_primes_sum variable.
                sqrt_up[i] -= (sqrt_up[d] - known_primes_sum) * prime
            else:
                # Here we can see why is it working so nice with the sqrt ranges :)
                # We can calculate it just because for any i: n // i is one of sqrt_down or sqrt_up
                sqrt_up[i] -= (sqrt_down[limit // d] - known_primes_sum) * prime

        # Updating the sqrt_down
        for i in range(limit_sqrt, prime_square - 1, -1):
            # Basically, we may iterate on the first sqrt(n) elements and update their's sum.
            # But, we may also note the indexes in the range(1, prime_square) would not be updated anymore !
            # Why ? because at this point sqrt_down does not contain the sum of numbers which divided by the primes
            # that are smaller than p, all the numbers below p * p are such numbers :)
            sqrt_down[i] -= (sqrt_down[i // prime] - known_primes_sum) * prime

    return sqrt_down, sqrt_up


def is_prime(n):
    """
    Check whether a given number is prime.

    Time Complexity: O(sqrt(n))
    Space Complexity: O(1)

    :param n: number to check
    :type n: int
    :return: True if n is prime, False otherwise.
    :rtype: bool
    """
    if n < 2:
        return False
    if n < 4:
        return True

    if not (n % 2 and n % 3):
        return False

    # From now and on, all divisors are of the form 6n+1/5.
    # If n is composite, there is have to be a prime divisor smaller than sqrt n.
    divisor = 5
    while divisor * divisor <= n:
        if not (n % divisor and n % (divisor + 2)):
            # Indicator for n composition
            return False

        divisor += 6

    return True


def is_miller_prime(n, rounds=100):
    """
    Using Miller-Rabin primary test to whether n is prime.

    Time Complexity: O(rounds * log(n) ^ 3) [log(n) ^ 3 because mul of 2 big numbers is O(log(n) ^ 2)]
    Space Complexity: O(1)

    :param n: number to check if prime.
    :type n: int
    :param rounds: chance for mistake is 1/4^number_of_rounds
    :type rounds: int
    :return: True if n is prime, otherwise, False.
    :rtype: bool
    """
    if n in [2, 3]:
        return True
    if n < 5:
        return False

    for _ in range(rounds):
        if _is_surely_composite(n, *omit_factor(n - 1, 2), randrange(2, n - 1)):
            # this answer is correct for sure
            return False

    # Because there is a lemma which claims that for a composite number has no more than
    # quarter prime witnesses, n is really prime in chance of 4^-rounds
    return True


def _is_surely_composite(n, d, s, a):
    """
    n-1 == 2 ** s * d
    If n is prime, then because of Fermat's little theorem and the trivial square root of 1 over Z[n] field:
        a ^ r == -1/1 mod n
        OR
        a ^ (r * 2^j) == -1 mod n for j in [0, s-1]
    """
    test_number = pow(a, d, n)
    if pow(a, d, n) in [1, n - 1]:
        # prime witness, a ** r == -1, 1 mod n
        return False

    for _ in range(s):
        test_number = pow(test_number, 2, n)
        if test_number == 1:
            # Because we cannot find prime witness up to now,
            # if n was prime, test_number could never be 1.
            # previous test_number was not -1/1 so in Zp the next test_number cannot be -1/1 as well :)
            return True

        if test_number == n - 1:
            # prime witness, a ** ((2 ** j) * r) == -1 mod n for j in [0, s-1]
            return False

    # there is no prime witness for sure.
    return True


def prime_nth_bounds(n):
    """
    Calculate the nth prime lower and upper bounds.
    NOTE: range size is n+-1.

    Time Complexity: O(1)
    Space Complexity: O(1)

    :param n: nth prime
    :type n: int
    :return: range which contains Pn
    :rtype: range
    """
    # Rosser's theorem:
    # log(n) + log(log(n)) - 1 < Pn / n < log(n) + log(log(n)) for n >= 6
    if n < 6:
        prime = [2, 3, 5, 7, 11][n-1]
        return range(prime, prime + 1)

    limiter = n * (log(n) + log(log(n)))
    return range(ceil(limiter) - n, floor(limiter))


def prime_nth(n):
    """
    Calculate the nth prime.

    Time Complexity: O(n*log(n))
    Space Complexity: O(n)

    :param n: nth prime
    :type n: int
    :return: Pn - the nth prime
    :rtype: int
    """
    bounds = prime_nth_bounds(n)
    primes = sieve_of_eratosthenes(bounds.stop)
    return primes[n - 1]
