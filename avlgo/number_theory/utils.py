

def power(base, exp, mod=None, identity=1):
    """
    Calculating exponent of different objects efficiently.
    The objects must support *,% operations.

    Time Complexity O(log(n))
    Space Complexity: O(1)

    :param base: base
    :param exp: exponent
    :param mod: modulo
    :param identity: the '1' in the given field.
    :return: base ^ exp % mod
    """
    pow_res = identity
    while exp:
        # scanning the binary representation of exp from LSB to the MSB.
        # base is the suitable base power of the current scanned bit.
        # If we got a turn on bit on exp, then we should add base to the result
        if exp & 1:
            pow_res *= base
            if mod:
                pow_res %= mod

        exp >>= 1
        base *= base
        if mod:
            base %= mod

    return pow_res


def omit_factor(n, factor):
    """
    Calculate the complement part of n relative to factor in n factorization.

    Time Complexity: O(log(n) / log(factor))
    Space Complexity: O(1)

    :param n: number to omit from
    :type n: int
    :param factor: factor to omit
    :type factor: int
    :return: {n // (base ^ p), max(p) s.t. factor^p|n}
    :rtype: tuple[int, int]
    """
    factor_pow = 0
    while n % factor == 0:
        factor_pow += 1
        n //= factor

    return n, factor_pow


def hadamard_product(a_vector, b_vector):
    """
    Calculates Hadamard product of two given vectors.

    Time Complexity: O(n)
    Space Complexity: O(n)

    :param a_vector: first vector
    :param b_vector: second vector
    :return: h_vector[i] = a_vector[i] * b_vector[i]
    """
    if len(a_vector) != len(b_vector):
        raise ValueError("A, B must be same sizes !")

    return [
        a * b for a, b in zip(a_vector, b_vector)
    ]


def scalar_product(a_vector, b_vector):
    """
    Calculates Scalar product (also known as dot product).

    Time Complexity: O(n)
    Space Complexity: O(n)

    :param a_vector: first vector
    :param b_vector: second vector
    :return: sigma{a_vector[i] * b_vector[i]}
    """
    return sum(hadamard_product(a_vector, b_vector))


def digit_sum(n, base=10, p=1, mod=None):
    """
    Calculate the digits sum in a given base.

    Time Complexity: O(log(n) * log(p) / log(base))
    Space Complexity: O(1)

    :param n: the number to sum digits
    :type n: int
    :param base: base to represent n in
    :type base: int
    :param p: sum the digit's pow
    :type p: int
    :param mod: calculates the result modulo mod
    :type mod: int
    :return: sum of digits to the power p in base modulo.
    :rtype: int
    """
    d_sum = 0
    while n:
        d_sum += power(n % base, p, mod)
        if mod:
            d_sum %= mod

        n //= base

    return d_sum


def recursive_digit_sum(n, base=10):
    """
    Calculate the sum of digits recursively.

    Time Complexity: O(1)
    Space Complexity: O(1)

    :param n: number to calculate sum of
    :type n: int
    :param base: base to sum in
    :type base: int
    :return: recursive digit sum in base
    :rtype: int
    """
    # Assuming n digits are N0 to Nk then n = sigma{Ni * base^i} for i=0 to k
    # Observing this sum modulo (base - 1) gives sigma{Ni} for i=0 to k (what we want recursively)
    if n == 0:
        return 0

    recursive_sum = n % (base - 1)
    if recursive_sum == 0:
        return base - 1

    return recursive_sum
