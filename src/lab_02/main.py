import time
from collections import Counter, defaultdict, deque
from functools import wraps
from typing import Callable

# --- data.py ---
products = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 1200, "quantity": 10},
    {"id": 2, "name": "Mouse", "category": "Electronics", "price": 25, "quantity": 50},
    {"id": 3, "name": "Desk Chair", "category": "Furniture", "price": 150, "quantity": 5},
    {"id": 4, "name": "Coffee Mug", "category": "Kitchen", "price": 10, "quantity": 100},
    {"id": 5, "name": "Monitor", "category": "Electronics", "price": 300, "quantity": 20},
]

# --- decorators.py ---
def benchmark(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"DEBUG: {func.__name__} executed in {end - start:.6f}s")
        return result
    return wrapper

# --- processors.py ---
def get_unique_categories(items: list[dict]) -> set[str]:
    return {item["category"] for item in items}

def group_by_category(items: list[dict]) -> dict[str, list[dict]]:
    res = defaultdict(list)
    for item in items:
        res[item["category"]].append(item)
    return dict(res)

def get_low_stock(items: list[dict], threshold: int) -> list[dict]:
    return [item for item in items if item["quantity"] < threshold]

# --- analytics.py ---
def calculate_total_inventory_value(items: list[dict]) -> float:
    return sum(item["price"] * item["quantity"] for item in items)

def find_most_expensive(items: list[dict]) -> dict:
    return max(items, key=lambda x: x["price"])

def create_price_filter(min_price: float) -> Callable[[dict], bool]:
    def filter_func(item: dict) -> bool:
        return item["price"] >= min_price
    return filter_func

def sum_prices(*prices: float) -> float:
    return sum(prices)

def create_product(**kwargs) -> dict:
    return kwargs

# --- main.py ---
def main():
    print("--- Analysis of Internet Shop (Variant 3) ---")
    
    # 1. Unique Categories (Set comprehension)
    cats = get_unique_categories(products)
    print(f"Categories: {cats}")

    # 2. Grouping
    grouped = group_by_category(products)
    print(f"Grouped: {list(grouped.keys())}")

    # 3. Total Value
    total = calculate_total_inventory_value(products)
    print(f"Total inventory value: ${total}")

    # 4. Search via Dict Index
    index = {p["id"]: p for p in products}
    print(f"Search ID 2: {index.get(2)}")

    # 5. Expensive Item (Lambda)
    expensive = find_most_expensive(products)
    print(f"Most expensive: {expensive['name']}")

    # 6. Low stock (List comprehension)
    low_stock = get_low_stock(products, 15)
    print(f"Low stock items: {[p['name'] for p in low_stock]}")

    # 7. Closure usage
    is_premium = create_price_filter(500)
    premium_items = [p for p in products if is_premium(p)]
    print(f"Premium items: {[p['name'] for p in premium_items]}")

    # 8. Args/Kwargs
    print(f"Sum of prices (args): {sum_prices(100, 200, 300)}")
    print(f"New product (kwargs): {create_product(name='Keyboard', price=50)}")

if __name__ == "__main__":
    main()