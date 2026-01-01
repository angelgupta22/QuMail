# bb84.py
"""
Simulated BB84 QKD module
Used as a key-generation backend for classical systems

Outputs:
- 256-bit shared secret key (bytes)

NOTE:
This is a simulation for hybrid / quantum-inspired systems.
"""

import secrets
import hashlib
from typing import List, Tuple

# -----------------------------
# Alice: generate bits & bases
# -----------------------------
def generate_alice(n: int) -> Tuple[List[int], List[int]]:
    bits = [secrets.randbelow(2) for _ in range(n)]
    bases = [secrets.randbelow(2) for _ in range(n)]  # 0=Z, 1=X
    return bits, bases


# -----------------------------
# Bob: measure bits
# -----------------------------
def generate_bob(
    alice_bits: List[int],
    alice_bases: List[int],
    channel_error: float
) -> Tuple[List[int], List[int]]:

    bob_bases = [secrets.randbelow(2) for _ in range(len(alice_bits))]
    bob_results = []

    for i in range(len(alice_bits)):
        if alice_bases[i] == bob_bases[i]:
            bit = alice_bits[i]
            if secrets.randbelow(10**6) / 10**6 < channel_error:
                bit ^= 1
            bob_results.append(bit)
        else:
            bob_results.append(secrets.randbelow(2))

    return bob_bases, bob_results


# -----------------------------
# Sifting
# -----------------------------
def sift(
    alice_bits: List[int],
    alice_bases: List[int],
    bob_bases: List[int],
    bob_results: List[int]
) -> Tuple[List[int], List[int]]:

    sifted_a, sifted_b = [], []
    for i in range(len(alice_bits)):
        if alice_bases[i] == bob_bases[i]:
            sifted_a.append(alice_bits[i])
            sifted_b.append(bob_results[i])
    return sifted_a, sifted_b


# -----------------------------
# QBER estimation
# -----------------------------
def estimate_qber(
    alice: List[int],
    bob: List[int],
    sample_fraction: float
) -> float:

    m = len(alice)
    sample_size = max(1, int(m * sample_fraction))
    positions = secrets.SystemRandom().sample(range(m), sample_size)

    errors = sum(
        1 for i in positions if alice[i] != bob[i]
    )
    return errors / sample_size


# -----------------------------
# Parity-based reconciliation
# -----------------------------
def parity(bits: List[int], start: int, end: int) -> int:
    p = 0
    for b in bits[start:end]:
        p ^= b
    return p


def reconcile(
    alice: List[int],
    bob: List[int],
    block_size: int = 16
) -> List[int]:

    bob = bob.copy()
    n = len(alice)

    for start in range(0, n, block_size):
        end = min(start + block_size, n)

        if parity(alice, start, end) != parity(bob, start, end):
            lo, hi = start, end
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if parity(alice, lo, mid) != parity(bob, lo, mid):
                    hi = mid
                else:
                    lo = mid
            bob[lo] = alice[lo]

    return bob


# -----------------------------
# Privacy amplification
# -----------------------------
def privacy_amplification(bits: List[int]) -> bytes:
    bitstring = ''.join(str(b) for b in bits)
    value = int(bitstring, 2)
    length = (len(bitstring) + 7) // 8
    raw = value.to_bytes(length, "big")
    return hashlib.sha256(raw).digest()


# -----------------------------
# Public API
# -----------------------------
def generate_qkd_key(
    num_bits: int = 2048,
    channel_error: float = 0.01,
    sample_fraction: float = 0.1,
    qber_threshold: float = 0.11
) -> bytes:
    """
    Main BB84 pipeline
    Returns: 256-bit key (bytes)
    """

    alice_bits, alice_bases = generate_alice(num_bits)
    bob_bases, bob_results = generate_bob(
        alice_bits, alice_bases, channel_error
    )

    sifted_a, sifted_b = sift(
        alice_bits, alice_bases, bob_bases, bob_results
    )

    qber = estimate_qber(
        sifted_a, sifted_b, sample_fraction
    )

    if qber > qber_threshold:
        raise RuntimeError("QBER too high — possible eavesdropping")

    reconciled_b = reconcile(sifted_a, sifted_b)
    final_key = privacy_amplification(sifted_a)

    return final_key
