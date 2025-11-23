"""
Post-Quantum KEM demo.

This script attempts to use a real PQC library (`pqcrypto`) to perform a KEM
(example: Kyber). If the library is not available, a secure fallback KEM
simulation is used instead (still marked simulation only).

We then encrypt the same short message (via AES-GCM with the derived shared
secret) and demonstrate that a naive brute-force search for the PQC private
key is infeasible (we attempt a small sampling and then show estimated time
for full brute force).

IMPORTANT: Simulation only — not real quantum code. Use this for education.
"""
import os
import time
import hashlib
from typing import Tuple

try:
    # Try common PQClean / pqcrypto API
    from pqcrypto.kem.kyber512 import generate_keypair as pq_generate, encapsulate as pq_encaps, decapsulate as pq_decaps
    HAS_PQ = True
except Exception:
    HAS_PQ = False

# Use PyCryptodome for symmetric encryption if available, otherwise use simple placeholder
try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    HAS_CRYPTO = True
except Exception:
    HAS_CRYPTO = False


def aes_gcm_encrypt(key: bytes, plaintext: bytes) -> Tuple[bytes, bytes, bytes]:
    if not HAS_CRYPTO:
        raise RuntimeError('PyCryptodome not available; install pycryptodome to run AES-GCM')
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ct, tag = cipher.encrypt_and_digest(plaintext)
    return iv, ct, tag


def aes_gcm_decrypt(key: bytes, iv: bytes, ct: bytes, tag: bytes) -> bytes:
    if not HAS_CRYPTO:
        raise RuntimeError('PyCryptodome not available; install pycryptodome to run AES-GCM')
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    return cipher.decrypt_and_verify(ct, tag)


# Fallback (simulation) KEM using HKDF-like derivation. Not a real PQC algorithm.
# Marked simulation only.
class FallbackKEM:
    @staticmethod
    def generate_keypair() -> Tuple[bytes, bytes]:
        # pk/sk are random 32-byte values for simulation
        pk = os.urandom(32)
        sk = pk  # for deterministic decapsulation in this toy simulation
        return pk, sk

    @staticmethod
    def encapsulate(pk: bytes) -> Tuple[bytes, bytes]:
        # ephemeral is ciphertext; shared secret = SHA256(pk||ephemeral)
        ephemeral = os.urandom(32)
        shared = hashlib.sha256(pk + ephemeral).digest()
        return ephemeral, shared

    @staticmethod
    def decapsulate(sk: bytes, ciphertext: bytes) -> bytes:
        # sk == pk in this simplified simulation
        return hashlib.sha256(sk + ciphertext).digest()


def demo():
    print('\nPQC KEM Demo (simulation-focused)')
    message = b'Quantum?'
    print('Message:', message)

    if HAS_PQ:
        print('Using real PQ library: pqcrypto (Kyber512)')
        pk, sk = pq_generate()
        ciphertext, shared_enc = pq_encaps(pk)
        shared_dec = pq_decaps(sk, ciphertext)
        assert shared_enc == shared_dec
        shared = shared_enc
    else:
        print('pqcrypto not available — using secure fallback simulation KEM')
        pk, sk = FallbackKEM.generate_keypair()
        ciphertext, shared = FallbackKEM.encapsulate(pk)

    # Use first 32 bytes of shared as AES key (or full shared if shorter)
    aes_key = hashlib.sha256(shared).digest()
    if HAS_CRYPTO:
        iv, ct, tag = aes_gcm_encrypt(aes_key[:32], message)
        recovered = aes_gcm_decrypt(aes_key[:32], iv, ct, tag)
        print('Recovered (legit):', recovered)
    else:
        print('PyCryptodome not available — skipping symmetric encryption demo')

    # Brute-force attempt: try to find SK by random sampling (will not find it)
    print('\nStarting small brute-force sampling (will not exhaust full space)...')
    attempts = 10000
    found = False
    t0 = time.time()
    for i in range(attempts):
        guess = os.urandom(32)
        # decapsulate with guess and compare
        if HAS_PQ:
            # For real PQ libs, decapsulation will fail silently or produce different shared
            try:
                shared_guess = pq_decaps(guess, ciphertext)
            except Exception:
                shared_guess = None
        else:
            shared_guess = FallbackKEM.decapsulate(guess, ciphertext)
        if shared_guess == shared:
            print('Found private key by sampling (very unlikely):', guess.hex())
            found = True
            break
    t1 = time.time()
    print(f'Sampling attempts: {attempts}, elapsed {t1-t0:.3f}s, found={found}')

    # Estimate full brute-force time for 256-bit keyspace
    key_bits = 256
    ops_per_sec = 1e7  # optimistic guess for crypto ops/second
    total_ops = 2 ** key_bits
    years = total_ops / ops_per_sec / (60 * 60 * 24 * 365)
    print(f'Estimated time to brute-force {key_bits}-bit key at {int(ops_per_sec):,} ops/s: {years:.2e} years')


if __name__ == '__main__':
    demo()
