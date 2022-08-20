

def power(base, exp, mod=None, identity=1):
    """
    Calculating exponent of different objects efficiently.
    The objects must support *,% operations.\

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
