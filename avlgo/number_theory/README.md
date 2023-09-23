# Number Theory #

# Co-Primes #
In `coprimes` module you can find methods for integers co-primes manipulations.
* `is_coprime`, `coprimes` - co-primes exact calculations.
* `euler_totient`, `euler_totient_range` - counting the number of co-primes numbers.
* `coprimes_sum`, `coprimes_sum_range` - summing the co-primes numbers.

## Diophantine Equation ##
The `diophantine_equation` module contains a set of core utils for solving Diophantine Equations.
* Solving modular equations
    * `linear_modular_equation` - simple modular equation
    * `chinese_remainder_linear_equation`, `chinese_remainder_equation`, `chinese_remainder_base` - advanced Chinese Reminder Theorem.
* Solving regular equations
    * `linear_equation` - simple generic equation solver.
    * `linear_equation_sol_counter` - advanced solution counter.
    

## Divisors ##
`divisors` is a simple module for advanced number divisors' calculation.
* `divisors` - enumerate all number divisors.
* `divisors_sum`, `divisors_sum_range`, `divisors_sum_range_sum` - advanced techniques for divisors sum by some power.
    * You may calculate the number of divisors using that method as well (zeroing power).
* `minimal_range_divisor` - the minimal number which divided by all numbers from 1 to n. 

## Fibonacci ##
`fibonacci` is a compact and cool module for useful fibonacci tricks (with logarithmic time complexity) :)
* `fibonacci_nth` - calculating the nth fibonacci efficiently.
* `fibonacci_sum`, `fibonacci_odd_sum`, `fibonacci_even_sum`, `fibonacci_square_sum` - advanced fibonacci sums.

## Integer Partition ##
`integer_partition` module exposed a set of variations for the way of writing n as a sum of positive integers.
* Integer Partition
    * `integer_partition`, `integer_partition_range` - classical calculation.
* Integer composition
    * `integer_compositions`, `integer_k_composition`, `integer_weak_k_composition` - classical calculation.
    * `integer_composition_forcing_k_range`, `integer_composition_forcing_non_k`, `integer_composition_forcing_k` - advanced methods.

## Inverse ##
`inverse` module is a simple one for calculating inverse numbers in modulo environment.
* `inverse_mod`, `inverse_prime_mod` - calculating inverse modulo using Euler's theorem.

## Primes ##
A very useful module is the `primes` module for advanced and core primes utils.
* `sieve_of_eratosthenes`, `sieve_of_atkin` - Top practical sieves for exact primes enumeration.
* `prime_sum_in_sqrt_ranges` - super advanced method for primes summing problems.
* `is_prime`, `is_miller_prime` - most useful primes testing.
* `prime_nth_bounds`, `prime_nth` - primes as a series.

## Primes Factorization ##
`primes_factorization` is a core module for numbers factorizations efficiently.
* `prime_exp`, `factorial_prime_exp`, `ncr_prime_exp` - single prime power calculation.
* `prime_factors`, `prime_factors_range` - classical algorithms.
* `ncr_prime_factors`, `triangular_prime_factors` - specific useful & efficient cases.

## Progression Sums ##
The `progression_sums` module contains simple series summing calculation.
* `arithmetic_progression_sum`
* `geometric_progression_sum`, `geometric_progression_inf_sum`
* `consecutive_progression_sum` - for specific powers.

## Pythagoras ##
Use `pythagoras` module for simple Pythagoras facts.
* `is_pythagorean_triple` - Pythagoras testing.
* `primitive_pythagorean_triple` - Pythagoras enumeration.

## Sequence nth ##
For generic sequence calculation, use the `sequence_nth` module
* `triangular_nth`, `pentagonal_nth`, `catalan_nth` - specific known sequences.
*  `linear_recursive_sequence_nth` - a strong tool for generic "linear recursive" sequence calculation.
