from typing import TypeGuard, TypeVar

K = TypeVar('K')
V = TypeVar('V')
def is_subdict(d1: dict, d2: dict[K, V]) -> TypeGuard[dict[K, V]]:
    return set(d1.items()).issubset(d2.items())

