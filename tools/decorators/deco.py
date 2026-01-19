from typing import Callable, Any
from functools import wraps

# decorator to transform output for functions that return a string
def output_transformer(transformer: Any):

    @wraps(transformer)
    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal transformer

            return transformer(func(*args, **kwargs))

        return wrapper

    return decorator

def output_formatter(symbol: str, before: bool):

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal symbol

            if before:
                return f'{symbol}{func(*args, **kwargs)}'
            else:
                return f'{func(*args, **kwargs)}{symbol}'

        return wrapper

    return decorator