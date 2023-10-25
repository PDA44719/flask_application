from app import prime_number_check


def test_primes():
    prime_values = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                    59, 61, 67, 71, 73, 79, 83, 89, 97]
    non_prime_values = [4, 6, 9, 15, 21, 24, 32, 45, 50]

    for prime in prime_values:
        assert prime_number_check(prime) is True

    for non_prime in non_prime_values:
        assert prime_number_check(non_prime) is False
