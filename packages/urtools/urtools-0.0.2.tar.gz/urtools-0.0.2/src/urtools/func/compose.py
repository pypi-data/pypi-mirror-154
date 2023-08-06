from functools import reduce
from typing import Callable, TypeVar, ParamSpec

def are_composable(f1: Callable, f2: Callable) -> bool:
    """Assert that the return type of `f1` matches the argument type of `f2`.
    """

    f1_return_type = f1.__annotations__['return']
    f2_first_argument_type = next(type_ for var, type_ in f2.__annotations__.items())
    f2_has_1_argument_type = len(f2.__annotations__) == 2
    
    return (f1_return_type == f2_first_argument_type) and f2_has_1_argument_type


P = ParamSpec('P')
R1, R2 = TypeVar('R1'), TypeVar('R2')
def compose2(f1: Callable[P, R1], f2: Callable[[R1], R2]) -> Callable[P, R2]:
    r"""Compose two functions.

    Composability does not need to be asserted  because it is typechecked.

    .. math::
        f &: \text{dom}\;f\to T\\
        g &: T\quad\quad\to \text{ran}\;g\\
        g\circ f &: A \quad\quad\to B
    """

    def composed(*args: P.args, **kwargs: P.kwargs) -> R2:
        return f2(f1(*args, **kwargs))
    
    return composed


R = TypeVar('R')
def compose(*functions: Callable) -> Callable[P, R]:
    """Compose any number of `functions` (or `Callable`s more generally) passed as a list.

    But first assert their composability.
    """

    assert len(functions) > 1, f"Provide at least two functions to compose. You provided {len(functions)} functions."
    assert all(are_composable(f1, f2) for f1, f2 in zip(functions, functions[1:]))
    
    def composed(*args: P.args, **kwargs: P.kwargs) -> R:
        identity = lambda x: x
        return reduce(compose2, functions, identity)(*args, **kwargs)

    return composed
