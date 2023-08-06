from typing import Callable, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')
def repeat(func: Callable[P, R], n: int) -> Callable[P, R]:
    new_func_str = "lambda x: {}x{}".format("f(" * n, ")" * n)
    new_func = eval(new_func_str, {"f": func})
    return new_func
