from typing import Iterable, TypeVar

from urtools.list.base import prune_list, reduce_list
from urtools.func import repeat
from urtools.type import is_nonstr_iter

def get_depth(x: object) -> int:
    """Get the depth of a given nested structure (lists and tuples)
    """
    if not is_nonstr_iter(x):
        return 0
    depths = [get_depth(x_inner) for x_inner in x
              if is_nonstr_iter(x_inner)]
    return max(depths)

T = TypeVar('T')
def pack1(x: T) -> list[T]:
    return [x]

def pack(x: object, depth_out: int | None=None) -> list:
    """Pack the input into a nested list of a given depth
    """
    if not is_nonstr_iter(x):
        x_packed = [x]
        depth_out = 0 if depth_out is None else depth_out
    else:
        x_packed = list(x)
        depth_out = 1 if depth_out is None else depth_out
    x_depth = get_depth(x_packed)
    return repeat(pack1, depth_out - x_depth)(x_packed)


def unpack(packed: Iterable, *,
           max_depth: int | None=None, prune: bool=False, depth: int=0) -> list:
    """Unpack an unpackable element (e.g. tuple or list)
     each unpackable element's sub-eleements are being moved to its super-/parent- element

    TODO: Expand, define behavior for some types, e.g. dictionaries
    """
    if not isinstance(packed, Iterable):
        raise AssertionError(f'`packed` must be an Iterable but is {type(packed)}; {packed=}')
    
    unpacked = [reduce_list(x) 
                if is_nonstr_iter(x) else x
                for x in packed]
    if prune:
        unpacked = prune_list(unpacked)

    if max_depth and depth < max_depth:
        return unpack(unpacked, max_depth=max_depth, prune=prune, depth=depth + 1)

    return unpacked