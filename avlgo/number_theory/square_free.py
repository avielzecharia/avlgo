from math import sqrt, ceil

from avlgo.number_theory.primes import sieve_of_eratosthenes


# TODO: Make it a generic sum function with power and mode
def square_free_counter(n):
    """
    Counting the number of `square free` number up to n.

    Time Complexity: O(~sqrt(n))
    Space Complexity: O(sqrt(n))

    :param n: limit to count to
    :type n: int
    :return: number of `square free` number up to n.
    :rtype: int
    """
    # The idea is to use the Inclusion–exclusion principle on the non square free numbers.
    # Which means, we count how much numbers are there which are divided by prime ^ 2 only.
    n_sqrt = ceil(sqrt(n))
    primes = sieve_of_eratosthenes(n_sqrt)

    sign = 1
    depth = 1
    combination_sum = 0
    combination_result = None
    while combination_result != 0:
        # We should basically stop for depth = {min(i) | P1 * P2 * ... * Pi > n} [i ~ ln(n)/ln(ln(n))]
        combination_result = _square_free_counter_comb(n, primes, depth, depth)

        # Inclusion–exclusion principle
        combination_sum += sign * combination_result
        sign *= -1
        depth += 1

    return n - combination_sum


def _square_free_counter_comb(n, primes, comb, depth, last_prime_ind=-1, multiplication=1):
    """
    Calculating the Inclusion–exclusion principle for all combinations of size comb using recursion.
    [The trivial solution for a fixed comb would be #comb iterative for loops]
    """
    # Every recursion depth level is simply a new "iterative for loop" over possible chosen primes.
    # Where the chosen primes are being chosen in increasing order (p1 > p2 > p3 > ...)
    # There are 2 main restrictions which limits the time complexity:
    #   1. The prime chosen in the depth'th for loop cannot exceed n ** (1/2*depth),
    #   because otherwise the #depth primes square multiplication exceed n.
    #   2. The current square primes multiplication cannot exceed a certain limit (multiplication_limiter),
    #   because if we had already used X primes multiplication, the next prime is greater than the max of the previous
    #   ones (which can be proved to be at least mul^(1/x)), therefore knowing we got more y iterations of primes
    #   greater than the current one, we can infer that we cannot exceed another limit based on current multiplication.
    if depth == 0:
        return n // (multiplication ** 2)

    result = 0
    prime_limiter = ceil(n ** (1/(2 * depth)))
    multiplication_limiter = ceil(n ** ((comb - depth + 1) / (2 * comb)))
    for prime_ind in range(last_prime_ind + 1, len(primes)):
        prime = primes[prime_ind]
        if prime > prime_limiter or multiplication * prime > multiplication_limiter:
            break

        tmp_result = _square_free_counter_comb(n, primes, comb, depth - 1, prime_ind, multiplication * prime)
        if tmp_result == 0:
            # The next calls from now and on will be 0 as well.
            break

        result += tmp_result

    return result

# TODO: mobius function, generating functions
