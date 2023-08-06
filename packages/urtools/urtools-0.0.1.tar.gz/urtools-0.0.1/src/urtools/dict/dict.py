from typing import Any, Callable, Iterable, Literal, TypeGuard, TypeVar

import pandas as pd

from urtools.string import partition_n
from urtools.list import pack

def filter_dict_nans(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None and v == v and str(v).lower() != 'nan'}
    
def df_to_jsonlist(df: pd.DataFrame) -> list[dict]:
    return [filter_dict_nans(record) for record in df.to_dict(orient='records')]

def join_dicts(dicts: Iterable[dict]) -> dict:
    joined_dict = {}
    for d in dicts:
        joined_dict.update(d)
    return joined_dict

K = TypeVar('K')
V = TypeVar('V')
def is_subdict(d1: dict, d2: dict[K, V]) -> TypeGuard[dict[K, V]]:
    return set(d1.items()).issubset(d2.items())

def sort_dict(d: dict[K, V], by: Literal['k', 'v', 'key', 'value'], *, 
              key: Callable | None=None, reverse: bool=False) -> dict[K, V]:
    if by[0] not in ['k', 'v']:
        raise AssertionError(f'Invalid argument {by=}')
    if by[0] == 'k':
        if all(isinstance(k, (int, float)) for k in d):
            return dict(sorted(d.items(), key=key, reverse=reverse))
        else:
            key_map = {str(k): k for k in d} | {k: str(k) for k in d}
            d_sorted = {key_map[k]: v 
                        for k, v in sorted(
                            [(key_map[k], v) 
                             for k, v in d.items()])}
            assert is_subdict(d_sorted, d)
            return d_sorted
    else:
        # by[0] == 'v':
        d_reversed = {v: k for k, v in d.items()}
        d_sorted = {k: v for v, k in sort_dict(d_reversed, by='k', key=key, reverse=reverse).items()}
        assert is_subdict(d_sorted, d)
        return d_sorted

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
