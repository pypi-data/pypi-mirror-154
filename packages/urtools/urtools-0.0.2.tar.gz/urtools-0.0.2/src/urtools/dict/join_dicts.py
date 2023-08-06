from typing import Iterable

def join_dicts(dicts: Iterable[dict]) -> dict:
    joined_dict = {}
    for d in dicts:
        joined_dict.update(d)
    return joined_dict
