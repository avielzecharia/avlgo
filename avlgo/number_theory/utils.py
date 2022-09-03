

def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm.

    Time Complexity: O(log(n))
    Space Complexity: O(1)

    :type a: int
    :type b: int
    :return: (x, y, gcd(a, b)) s.t. a * x + b * Y = gcd(a, b)
    :rtype: tuple[int, int, int]
    """
    # r(0), r(1) = a, b
    # s(0), t(0) = 1, 0
    # s(1), t(1) = 0, 1
    old_r, r = a, b
    old_s, old_t = 1, 0
    s, t = 0, 1

    while r != 0:
        # q = r(i) / r(i+1)
        q = old_r // r

        # r(i) = q * r(i+1) + r(i+2) -> r(i+2) = r(i) - q * r(i+1)
        old_r, r = r, old_r - q * r

        # r(i+2) = a * s(i+2) + b * t(i+2)
        # r(i+2) = r(i) - q * r(i+1) = [a * s(i) + b * t(i)] - [a * s(i+1) + b * t(i+1)] * q =
        # a * [s(i) - s(i+1) * q] + b * [t(i) - t(i+1) * q]
        # -> s(i+2) = s(i) - s(i+1) * q
        # -> t(i+2) = t(i) - t(i+1) * q
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    # since r=0, gcd(a, b) = old_r and old_r = a * old_s + b * old_t = gcd(a, b)
    return old_s, old_t, old_r


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
        d_sum += pow(n % base, p, mod)
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


# That is a very coll trick because we can create a lot of cool polynomials to calculates complicated sums efficiently.
def power_set_sum(elements, p=1, mod=None):
    """
    Calculate the sum of the inner multiply of all subset of elements.

    Time Complexity: O(#elements)
    Space Complexity: O(1)

    :param elements: iterable object of elements
    :type elements: list|set
    :param mod: return the result modulo mod
    :type mod: int
    :param p: refer each element as element ^ p
    :type p: int
    :return: SUM(PI(S)^p) for S in power_set(elements)
    """
    pow_sum = 1
    for element in elements:
        # The trick is to calculate the polynomial (e0^p + 1) * ... (en^p + 1)
        # So, all the possible combinations multiplies will be summed.
        pow_sum *= power(element, p, mod=mod) + 1
        if mod:
            pow_sum %= mod

    return pow_sum - 1
