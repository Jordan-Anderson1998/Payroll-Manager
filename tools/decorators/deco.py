from typing import Callable, Any

# decorator to transform output for functions that return a string
def output_transformer(transformer: Any):

    def decorator(func: Callable) -> Callable:

        def wrapper(*args, **kwargs):
            nonlocal transformer

            return transformer(func(*args, **kwargs))

        return wrapper

    return decorator