import json
from functools import wraps
from typing import Callable, Dict

def handle_file_operations(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(f"Change file not found")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON format in file")
            return {}
        except Exception as e:
            print(f"Unexpected error reading change file: {str(e)}")
            return {}
    return wrapper