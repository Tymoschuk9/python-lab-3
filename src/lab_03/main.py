import csv
import random
import tracemalloc
import time
from pathlib import Path
from collections import Counter
from itertools import islice, chain, accumulate, pairwise
from typing import NamedTuple, Iterator, Iterable, Any

# --- Data Model ---
class ProductRecord(NamedTuple):
    product_id: int
    name: str
    category: str
    price: float
    quantity: int

# --- Iterator (Custom) ---
class ProductIterator:
    def __init__(self, data: list):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        result = self.data[self.index]
        self.index += 1
        return result

# --- Generators ---
def read_lines(path: Path) -> Iterator[str]:
    with path.open("r", encoding="utf-8") as file:
        yield from file

def parse_csv(lines: Iterable[str]) -> Iterator[dict]:
    reader = csv.DictReader(lines)
    yield from reader

def validate_products(rows: Iterable[dict]) -> Iterator[ProductRecord]:
    for row in rows:
        try:
            yield ProductRecord(
                int(row["product_id"]),
                row["name"].strip(),
                row["category"].strip(),
                float(row["price"]),
                int(row["quantity"])
            )
        except (ValueError, KeyError):
            continue

def filter_by_category(products: Iterable[ProductRecord], category: str) -> Iterator[ProductRecord]:
    for p in products:
        if p.category == category:
            yield p

def batched(iterable: Iterable, size: int) -> Iterator[list]:
    it = iter(iterable)
    while True:
        batch = list(islice(it, size))
        if not batch: break
        yield batch

# --- Analytics ---
def calculate_store_stats(products: Iterable[ProductRecord]):
    total_val = 0.0
    max_price = 0.0
    count = 0
    for p in products:
        total_val += (p.price * p.quantity)
        if p.price > max_price: max_price = p.price
        count += 1
    return total_val, max_price, count

# --- Eager vs Lazy Comparison ---
def run_eager(path: Path):
    with path.open() as f:
        data = list(csv.DictReader(f))
        return [p for p in data if float(p['price']) > 100]

def run_lazy(path: Path):
    lines = read_lines(path)
    products = validate_products(parse_csv(lines))
    return (p for p in products if p.price > 100)

# --- Test Generator ---
def generate_test_file(path: Path, count: int):
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "name", "category", "price", "quantity"])
        for i in range(count):
            writer.writerow([i, f"Product {i}", random.choice(["Tech", "Food", "Home"]), round(random.uniform(10, 500), 2), random.randint(1, 100)])

def main():
    path = Path("data/products.csv")
    generate_test_file(path, 100000)

    # Demonstrate Lazy Pipeline
    pipeline = filter_by_category(validate_products(parse_csv(read_lines(path))), "Tech")
    first_3 = list(islice(pipeline, 3))
    print(f"First 3 Tech products: {first_3}")

    # Memory Check
    tracemalloc.start()
    _ = list(run_lazy(path))
    _, peak = tracemalloc.get_traced_memory()
    print(f"Lazy Peak Memory: {peak / 1024:.2f} KB")
    tracemalloc.stop()

if __name__ == "__main__":
    main()