import json
import os
from decorators.file_exceptions import handle_file_operations
from typings.change_types import Change

__location__ = os.path.realpath(
os.path.join(os.getcwd(), os.path.dirname(__file__)))

@handle_file_operations
def get_change_from_file(path_to_file='change.json') -> Change:
    with open(os.path.join(__location__, path_to_file), "r") as product_file:
        change_file = json.load(product_file)
        return { int(key): val for key,val in change_file.items() }

@handle_file_operations
def save_change_to_file(change: Change, path_to_file='change.json'):
    print(f"Saving change state with: {change}")
    with open(os.path.join(__location__, path_to_file), "w", encoding='utf-8') as product_file:
        json.dump(change, product_file)
