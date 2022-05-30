def get_primes(limit):
    # sieve of eratosthenes
    a = [True] * (limit+1)  # Initialize the primality list
    a[0] = False  # 0 is not a prime
    a[1] = False  # 1 is not a prime
    primes = []
    for (i, isprime) in enumerate(a):
        if isprime:
            primes.append(i)
            for n in range(i * i, limit+1, i):  # Mark factors non-prime
                a[n] = False
    return primes


def prime_factorization(n):
    primes = get_primes(n)
    factors = []
    while n > 1:
        for prime in primes:
            if n % prime == 0:
                factors.append(prime)
                n /= prime
                continue
    return factors


print(prime_factorization(22))
print(prime_factorization(23))
