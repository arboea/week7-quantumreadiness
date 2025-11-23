"""
RSA toy demo (simulation only).

This file generates a small RSA keypair (toy sizes), encrypts a short message,
then demonstrates a brute-force/factor attack that recovers the private key.

IMPORTANT: Simulation only — not real quantum code. Do NOT use these tiny
parameters for real security. This is educational code only.
"""
import math
import random
from typing import Tuple


def is_probable_prime(n: int, k: int = 8) -> bool:
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n % p == 0:
            return n == p

    # Miller-Rabin
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def try_composite(a: int) -> bool:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    for _ in range(k):
        a = random.randrange(2, n - 1)
        if try_composite(a):
            return False
    return True


def generate_prime(bits: int) -> int:
    while True:
        p = random.getrandbits(bits) | 1
        if is_probable_prime(p):
            return p


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)


def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError('modular inverse does not exist')
    return x % m


class RSAKeypair:
    def __init__(self, p: int, q: int, e: int = 65537):
        self.p = p
        self.q = q
        self.n = p * q
        phi = (p - 1) * (q - 1)
        if math.gcd(e, phi) != 1:
            raise ValueError('e and phi(n) not coprime')
        self.e = e
        self.d = modinv(e, phi)


def int_from_bytes(b: bytes) -> int:
    return int.from_bytes(b, byteorder='big')


def int_to_bytes(i: int) -> bytes:
    length = (i.bit_length() + 7) // 8
    return i.to_bytes(length, byteorder='big')


def rsa_encrypt(m_bytes: bytes, pub_n: int, pub_e: int) -> int:
    m = int_from_bytes(m_bytes)
    if m >= pub_n:
        raise ValueError('message too large for modulus')
    return pow(m, pub_e, pub_n)


def rsa_decrypt(cipher: int, priv_d: int, priv_n: int) -> bytes:
    m = pow(cipher, priv_d, priv_n)
    return int_to_bytes(m)


def brute_force_factor(n: int) -> Tuple[int, int]:
    # Very naive trial-division factoring for toy demonstration
    lim = int(math.isqrt(n)) + 1
    for a in range(2, lim):
        if n % a == 0:
            return a, n // a
    raise ValueError('failed to factor n')


def demo():
    print('\nRSA Toy Demo (simulation only)')
    # Use very small keys so factoring is fast in demonstration
    bits = 16
    p = generate_prime(bits)
    q = generate_prime(bits)
    # Ensure p != q
    while q == p:
        q = generate_prime(bits)
    e = 65537
    try:
        keypair = RSAKeypair(p, q, e=e)
    except ValueError:
        # If e and phi not coprime, pick a small e
        e = 17
        keypair = RSAKeypair(p, q, e=e)

    print(f'Generated small RSA key: n={keypair.n} (bits ~{keypair.n.bit_length()})')

    message = b'Quantum?'  # short message
    print('Original message:', message)
    cipher = rsa_encrypt(message, keypair.n, keypair.e)
    print('Ciphertext (int):', cipher)

    # Legitimate decryption
    recovered = rsa_decrypt(cipher, keypair.d, keypair.n)
    print('Decrypted (legit):', recovered)

    # Attack: factor n
    print('\nStarting naive factor attack (trial division)...')
    p_found, q_found = brute_force_factor(keypair.n)
    print(f'Found factors p={p_found}, q={q_found}')
    phi = (p_found - 1) * (q_found - 1)
    d_recovered = modinv(keypair.e, phi)
    recovered_attack = rsa_decrypt(cipher, d_recovered, keypair.n)
    print('Decrypted (attack):', recovered_attack)


if __name__ == '__main__':
    demo()
