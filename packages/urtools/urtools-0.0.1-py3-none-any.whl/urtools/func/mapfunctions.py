from typing import Callable, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')
def mapfunctions(functions: list[Callable[P, R]], *args: P.args, **kwargs: P.kwargs) -> list[R]:
    return [f(*args, **kwargs) for f in functions]

