from collections.abc import Iterable
from itertools import islice


def chunk_generator(iterable: Iterable, n: int):
    it = iter(iterable)
    while chunk := list(islice(it, n)):
        yield chunk
