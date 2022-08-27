import operator
from functools import reduce
from math import gcd

from avlgo.number_theory.inverse import inverse_mod
from avlgo.number_theory.utils import extended_gcd, scalar_product


def linear_modular_equation(a, b, m):
    """
    Solving the diophantine equation aX = b (mod m).

    Time Complexity: O(log(a) + log(m))
    Space Complexity: O(1)

    :type a: int
    :type b: int
    :type m: int
    :return: range of all solutions X if exist.
    :rtype: range
    """
    # We can solve the equation aX + mY = b, iff aX = b (mod m) where X is our solution.
    # d = gcd(a, m) -> as we know, (X + m/d) is also a solution - we got total d different solutions !
    x, y = linear_equation([a, m], b)
    return range(x, x + m, m // gcd(a, m))


def linear_equation(coefficients, value):
    """
    Solving the diophantine equation `sigma{Ci * Xi} = value`.

    Time Complexity: O(#coefficient * log(max(coefficient)))
    Space Complexity: O(#coefficient)

    :param coefficients: equation coefficients
    :type coefficients: list[int]
    :param value: equation value
    :type value: int
    :return: possible integer's vector solution for the equation.
    :rtype: list[int]
    """
    if not coefficients:
        raise NoIntegerSolution("No coefficients supplied")

    # C0 * X0 + C1 * X1 + ... + Ck * Xk = v, C0*Y0 + C1*Y1 = gcd(C0, C1) [keep Y0, Y1]
    # gcd(C0, C1) * Z + C2 * X2 + ... + Ck * Xk = v, gcd(C0, C1)*Y2 + C2*Y3 = gcd(C0, C1) [keep Y2, Y3]
    # Using Y's, if I will find out Z, then X0 = Y0 * Z and X1 = Y1 * Z
    # ... [keep Y's]
    coefficients_gcd = coefficients[0]
    y_memory = []
    for coefficient in coefficients:
        y0, y1, coefficients_gcd = extended_gcd(coefficients_gcd, coefficient)
        y_memory.append((y0, y1))

    if value % coefficients_gcd:
        raise NoIntegerSolution("value must be divided by coefficients GCD")

    # gcd(C0, ..., Ck) * Z = v -> Z = v / gcd(C0, ..., Ck).
    # - Back calculation with Y's assuming Xi -
    z = value // coefficients_gcd
    solution = []
    for y0, y1 in reversed(y_memory):
        solution.insert(0, z * y1)
        z *= y0

    return solution


def chinese_remainder_linear_equation(a_vector, b_vector, m_vector):
    """
    Solve chinese remainder linear equation.
    Find root such that aiX = bi mod mi for all vectors elements.
    Note: all gcd(a, m) elements have to be co-primes in pairs.

    Time Complexity: O(#vector * log(n))
    Space Complexity: O(#vector)

    :type a_vector: list[int]
    :type b_vector: list[int]
    :type m_vector: list[int]
    :return: root which satisfies the modular equation requirements.
    :rtype: int
    """
    # we can solve every single equation: aiX = bi mod mi,
    # and convert it to the form X = SOL mod (mi // gcd(ai, mi)).
    modulo_vector = []
    values_vector = []
    for a, b, m in zip(a_vector, b_vector, m_vector):
        range_solution = linear_modular_equation(a, b, m)
        values_vector.append(range_solution.start)
        modulo_vector.append(range_solution.step)

    return chinese_remainder_equation(values_vector, modulo_vector)


def chinese_remainder_equation(a_vector, m_vector):
    """
    Solve chinese remainder equation.
    Find root such that X = ai mod mi for all vectors elements.
    Note: all M elements have to be co-primes in pairs.

    Time Complexity: O(#vector * log(n))
    Space Complexity: O(#vector)

    :type a_vector: list[int]
    :type m_vector: list[int]
    :return: root which satisfies the modular equation requirements.
    :rtype: int
    """
    # This is basically a bijection function Z(m0, ..., mk) -> Z(m)
    # More than that, it is a bijection function coprimes Z(m0, ..., mk) -> coprimes Z(m)
    # The other direction Z(m) -> Z(m0, ..., mk) could be achieved by ai = x % mi.
    # -
    # After we got that unique base, all we have to do is to attach the ith elements of a_vector and base
    # We may return the result mod m, because every two different solution are equal modulo m.
    # Proof: for X, Y solutions -> mi|X-Y for all i -> M|X-Y -> x = y mod m
    m = reduce(operator.mul, m_vector)
    return scalar_product(
        a_vector,
        chinese_remainder_base(m_vector)
    ) % m


def chinese_remainder_base(m_vector):
    """
    Calculates the base for the chinese remainder theorem.
    Base vector such that base[i] % mj = 1 if i=j, else 0 for all i, j.

    Time Complexity: O(#vector * log(n))
    Space Complexity: O(#vector)

    :param m_vector:
    :return: base[i] = M/mi * inverse_d(M/mi, mi)
    """
    # The following base meets the requirements: base[i] = M/mi * inverse_mod(M/mi, mi)
    m = reduce(operator.mul, m_vector)
    return [
        (m // m_i) * inverse_mod(m // m_i, m_i)
        for m_i in m_vector
    ]


class NoIntegerSolution(Exception):
    pass


# TODO: Pell-like equations
