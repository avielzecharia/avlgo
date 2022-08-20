from avlgo.number_theory.math_series import linear_recursive_series_nth


def fibonacci_nth(n, mod=None):
    """
    Calculate the nth element in the Fibonacci sequence.
    F0 = 0, F1 = 1, Fn = Fn-1 + Fn-2

    Time Complexity: O(log(n))
    Space Complexity: O(1)

    :param n: index
    :type n: int
    :param mod: calculate Fn % mod
    :type mod: int
    :return: Fn
    :rtype: int
    """
    return linear_recursive_series_nth(
        n,
        coefficients=[1, 1],
        base_cases=[0, 1],
        mod=mod
    )


def fibonacci_sum(n, mod=None):
    """
    Calculate the sum of the first n fibonacci numbers.

    Time Complexity: O(log(n))
    Space Complexity: O(1)

    :param n: number of elements to sum
    :type n: int
    :param mod: calculate SUM % mod
    :return: sigma{Fi} i=0 to n
    :rtype: int
    """
    # F0   = F2   - F1
    # F1   = F3   - F2
    # F2   = F4   - F3
    # ...
    # Fn-1 = Fn+1 - Fn
    # Fn   = Fn+2 - Fn+1
    # ----------------------
    # Sigma Fn = Fn+2 - F1 = Fn+2 - 1
    fib_sum = fibonacci_nth(n+2, mod) - 1

    return fib_sum % mod if mod else fib_sum


def fibonacci_odd_sum(n, mod=None):
    """
    Calculate the sum of the first n odd indexes fibonacci numbers.

    Time Complexity: O(log(n))
    Space Complexity: O(1)

    :param n: number of odd index elements to sum
    :type n: int
    :param mod: calculate SUM % mod
    :type mod: int
    :return: sigma{F[2i-1]} for i=1 to n
    :rtype: int
    """
    # F2n = F2n-1 + F2n-2 =
    #     = F2n-1 + F2n-3 + F2n-4 =
    #     = ... =
    #     = F2n-1 + F2n-3 + ... + F3 + F1 + F0 =
    #     = 0 + F1 + F3 + ... + F2n-1
    return fibonacci_nth(2 * n, mod)


def fibonacci_even_sum(n, mod=None):
    """
    Calculate the sum of the first n even indexes fibonacci numbers.

    Time Complexity: O(log(n))
    Space Complexity: O(1)

    :param n: number of even index elements to sum
    :type n: int
    :param mod: calculate SUM % mod
    :type mod: int
    :return: sigma{F[2i]} for i=1 to n
    :rtype: int
    """
    # F2n+1 = F2n + F2n-1 =
    #       = F2n + F2n-2 + F2n-3 =
    #       = ... =
    #       = F2n + F2n-2 + ... + F4 + F2 + F1 =
    #       = 1 + F2 + F4 + ... + F2n
    even_sum = fibonacci_nth(2 * n + 1, mod) - 1

    return even_sum % mod if mod else even_sum


def fibonacci_square_sum(n, mod=None):
    """
    Calculate the sum of squares the first n indexes fibonacci numbers.

    Time Complexity: O(log(n))
    Space Complexity: O(1)

    :param n: number of index elements to sum
    :type n: int
    :param mod: calculate SUM % mod
    :type mod: int
    :return: sigma{Fi^2} for i=1 to n
    :rtype: int
    """
    # Fi ^ 2 = (Fi+1 - Fi-1) * Fi = Fi+1 * Fi - Fi-1 * Fi
    # ----------------------
    # F1 ^ 2 = F2 * F1 - F0 * F1
    # F2 ^ 2 = F3 * F2 - F1 * F2
    # ...
    # ----------------------
    # Sigma Fn ^ 2 = Fn+1 * Fn - F0 * F1 = Fn+1 * Fn
    square_sum = fibonacci_nth(n, mod) * fibonacci_nth(n + 1, mod)

    return square_sum % mod if mod else square_sum
