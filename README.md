Quick demos for RSA toy and PQC simulation.

Files:
- `quantum_examples/rsa_toy.py`: Toy RSA keygen, encrypt, and naive factor attack.
- `quantum_examples/pqc_example.py`: Attempts to use `pqcrypto` (Kyber) or falls back to a simulation that shows brute forcing is infeasible.

Install optional deps:

```powershell
python -m pip install -r requirements.txt
```

Run demos:

```powershell
python quantum_examples/rsa_toy.py
python quantum_examples/pqc_example.py
```
