**RSA Toy Attack — Summary**

**Simulation only — do not use these parameters in production.**

Context
- This repository contains a small educational demonstration (`quantum_examples/rsa_toy.py`) that generates intentionally tiny RSA keypairs, encrypts a short message, and recovers the private key by factoring the modulus `n = p * q` using a naive trial-division algorithm.

Attack method (what we did)
- For each RSA instance the attack performs simple trial division: iterate a from 2..sqrt(n) and check `n % a == 0`. When a factor is found, compute the other factor `q = n // a`.
- Once `p` and `q` are known compute `phi = (p-1)*(q-1)` and the private exponent `d = e^{-1} mod phi` (modular inverse). Decrypt ciphertext using `m = c^d mod n`.

Complexity and limits
- Trial division worst-case cost is O(sqrt(n)) arithmetic steps (roughly proportional to the square root of the modulus). If `n` is a product of two k-bit primes, `sqrt(n)` ~ 2^k — so the attacker work grows exponentially in the prime bit-length.
- For toy primes (12–20 bits each) sqrt(n) is tiny and factoring finishes in milliseconds. For realistic RSA (e.g., 2048-bit modulus where each prime is ~1024 bits) naive trial division is impossible: sqrt(n) ~ 2^1024 operations.
- Shor's algorithm (quantum) would dramatically change the landscape by factoring in polynomial time — the toy demonstrates the principle of brokenness, not the quantum algorithm itself.

Empirical results (from the repo runs)
- We ran factoring on random toy keys with prime sizes 12, 14, 16, 18, 20 bits. All ciphertexts were recovered.
- Example timings (wall-clock on developer machine; results stored at `visualizations/rsa_bruteforce_results.txt`):
  - 12-bit primes: factoring time ~ 0.0013 s — decryption succeeded
  - 14-bit primes: factoring time ~ 0.00044 s — decryption succeeded
  - 16-bit primes: factoring time ~ 0.00237 s — decryption succeeded
  - 18-bit primes: factoring time ~ 0.00118 s — decryption succeeded
  - 20-bit primes: factoring time ~ 0.00061 s — decryption succeeded
- Timings vary due to where the small factor appears in the search and random prime distribution; they are illustrative only.

What this shows
- Small RSA parameters are trivial to break using classical brute-force factoring — that's why real systems use large primes and carefully-vetted implementations.
- The demonstration also illustrates the "harvest-now, decrypt-later" threat: adversaries may record encrypted traffic now and decrypt it later if cryptography becomes breakable (classic or quantum).

Mitigation and recommendations
- Do not use small parameters — follow current best-practice key sizes (e.g., RSA 2048+ where still required, though migrating away from RSA is recommended).
- Use ephemeral keys / forward secrecy (e.g., ECDHE) so recorded sessions cannot be decrypted later using a compromised static key.
- Plan and begin migration to Post-Quantum Cryptography (PQC) for long-term confidentiality, following a staged approach: inventory, pilots, hybrid deployments, KMS/HSM integration, key rotations.
- Maintain an inventory of long-lived encrypted archives and consider re-encrypting high-risk archived data with PQC-resistant algorithms.

Files & artifacts
- Demo code: `quantum_examples/rsa_toy.py`
- Experimental results: `visualizations/rsa_bruteforce_results.txt`
- Demo outputs and visualization: `visualizations/demo_outputs.txt`, `visualizations/demo_summary.png`
- PQC notes and plan: `Quantum_Readiness.md`

References & further reading
- NIST Post-Quantum Cryptography project: https://csrc.nist.gov/projects/post-quantum-cryptography
- Practical guides to key management and forward secrecy (vendor docs and RFCs).

End of summary
