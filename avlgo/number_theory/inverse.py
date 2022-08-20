from avlgo.number_theory.utils import extended_gcd


# Another approach could be using Euler's theorem -> a^-1 = a^(phi(m)-1) % m,
# but calculate phi(m) is expensive in time - O(sqrt(n)).
def inverse_mod(a, mod):
    """
    Calculation the inverse of a in mod field.

    Time Complexity: O(log(n))
    Space Complexity: O(1)

    :type a: int
    :type mod: int
    :return: a^-1 % mod
    :rtype: int
    """
    a_inverse, mod_inverse, gcd_a_mod = extended_gcd(a, mod)
    if gcd_a_mod != 1:
        raise ValueError("a, mod are not coprime numbers !")

    return a_inverse % mod


def inverse_prime_mod(a, prime):
    """
    Calculation the inverse of a over Z[prime].

    Time Complexity: O(log(n))
    Space Complexity: O(1)

    :type a: int
    :type prime: int
    :return: a^-1 % prime
    """
    # Using Fermat's little theorem ->
    # If p not divide a, then a ^ (p - 1) = 1 mod p
    if a % prime == 0:
        raise ValueError("a is divisible by prime !")

    return pow(a, prime - 2, mod=prime)
