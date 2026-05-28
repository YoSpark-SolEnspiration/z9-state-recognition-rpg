import hashlib
import random

def stable_int_seed(*parts: str) -> int:
    """
    Deterministic seed from concatenated string parts.
    """
    s = "|".join(parts).encode("utf-8")
    h = hashlib.sha256(s).hexdigest()
    return int(h[:8], 16)  # 32-bit seed

def rng_for(*parts: str) -> random.Random:
    return random.Random(stable_int_seed(*parts))
