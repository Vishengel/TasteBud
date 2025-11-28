import hashlib
from collections.abc import Iterable
from itertools import islice


def chunk_generator(iterable: Iterable, n: int):
    it = iter(iterable)
    while chunk := list(islice(it, n)):
        yield chunk


def get_sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()
