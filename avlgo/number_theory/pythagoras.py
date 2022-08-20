

def is_pythagorean_triple(a, b, c):
    """
    Check whether (a, b, c) is a Pythagorean triple.

    Time Complexity: O(1)
    Space Complexity: O(1)

    :type a: int
    :type b: int
    :type c: int
    :rtype: bool
    """
    return a ** 2 + b ** 2 == c ** 2


def primitive_pythagorean_triple(m, n):
    """
    Generate a new primitive Pythagorean triple based on 2 seed numbers.
    NOTE: m, n must be coprime, and exactly one of them is even.

    Time Complexity: O(1)
    Space Complexity: O(1)

    :type m: int
    :type n: int
    :return: (a, b, c) primitive Pythagorean triple
    """
    # All primitive Pythagorean triples can be generated by:
    # a = m ^ 2 - n ^ 2, b = 2mn, c = m ^ 2 + n ^ 2
    # where m > n > 0 and m, n are coprime, and exactly one of them is even.
    return m ** 2 - n ** 2, 2 * m * n, m ** 2 + n ** 2