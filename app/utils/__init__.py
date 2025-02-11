# app/utils/__init__.py

import hashlib

def generate_cache_key(data: str) -> str:
    """
    Generates a cache key from a given string by hashing it.
    """
    return hashlib.md5(data).hexdigest()
