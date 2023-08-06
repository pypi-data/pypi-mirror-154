from typing import Any, Iterable, TypeVar

from urtools.dict.join_dicts import join_dicts

K = TypeVar('K')
V = TypeVar('V')
Keys = list[K]
def _dict_multindex_prep_keys(d: dict[K, Any], keys: K | Iterable[K] | None=None, *,
                              neg_keys: K | Iterable[K] | None=None) -> Keys:
    keys = list(keys) if keys is not None else list(d) #type:ignore
    neg_keys = set(list(neg_keys)) if neg_keys is not None else set() #type:ignore
    keys = list(set(keys).difference(neg_keys))
    return keys
    
def dict_multindex(d: dict[K, V], keys: K | Iterable[K] | None=None, *,
                   neg_keys: K | Iterable[K] | None=None) -> dict[K, V]:
    # PREP KEYS:
    keys = _dict_multindex_prep_keys(d, keys=keys, neg_keys=neg_keys)
    return {k: d[k] for k in keys}

def dict_del_keys(d: dict[K, V], del_keys: Iterable[K]) -> dict[K, V]:
    return {k: v for k, v in d.items() if k not in del_keys}
    
def dict_list_index(d_list: Iterable[dict[K, V]], k: K) -> list[V | None]:
    return [d.get(k) for d in d_list]

def dict_list_multindex(d_list: Iterable[dict[K, V]], keys: K | Iterable[K] | None=None, *,
                        neg_keys: K | Iterable[K] | None=None) -> dict[K, list[V]]:
    if not d_list:
        return {}
    keys = _dict_multindex_prep_keys(d=join_dicts(d_list), keys=keys, neg_keys=neg_keys)    
    return {k: [d[k] for d in d_list if k in d]
            for k in keys}
