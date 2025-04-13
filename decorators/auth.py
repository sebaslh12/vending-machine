from functools import wraps
from typing import Callable

def auth_decorator(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs) -> bool:
        print("Logged in Successfully")
        return func(*args, **kwargs)

    return wrapper