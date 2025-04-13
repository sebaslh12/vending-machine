import json
import os
from decorators.file_exceptions import handle_file_operations
from typings.product_types import Products

__location__ = os.path.realpath(
os.path.join(os.getcwd(), os.path.dirname(__file__)))

@handle_file_operations
def get_products_from_file(path_to_file='products.json') -> Products:
    with open(os.path.join(__location__, path_to_file), "r") as product_file:
        return json.load(product_file)

@handle_file_operations
def save_products_to_file(products: Products, path_to_file='products.json') -> None:
    print(f"Saving product state with: {products}")
    with open(os.path.join(__location__, path_to_file), "w", encoding='utf-8') as product_file:
        json.dump(products, product_file)

