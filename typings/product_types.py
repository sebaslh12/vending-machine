from typing import TypedDict, Dict

class ProductInfo(TypedDict):
    price: int
    quantity: int


Products = Dict[str, ProductInfo]