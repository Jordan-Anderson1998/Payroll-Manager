from typing import Callable, Any

# decorator to transform output for functions that return a string
def output_transformer(transformer: Any):

    def decorator(func: Callable) -> Callable:

        def wrapper(*args, **kwargs):
            nonlocal transformer

            return transformer(func(*args, **kwargs))

        return wrapper

    return decorator

def output_formatter(symbol: str, before: bool):

    def decorator(func: Callable) -> Callable:

        def wrapper(*args, **kwargs):
            nonlocal symbol

            if before:
                return f'{symbol}{func(*args, **kwargs)}'
            else:
                return f'{func(*args, **kwargs)}{symbol}'

        return wrapper

    return decorator

