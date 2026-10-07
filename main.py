try:
    from lab_01.models import Product
except ImportError:
    from dataclasses import dataclass
    @dataclass
    class Product:
        name: str
        category: str
        price: float
        quantity: int
        total_value: float

import csv
import itertools
from typing import Iterable, Iterator, Generator

def read_products_lazy(file_path: str) -> Generator[Product, None, None]:
    """Генератор для потокового читання великого файлу (lazy loading)."""
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield Product(
                name=row['name'],
                category=row['category'],
                price=float(row['price']),
                quantity=int(row['quantity']),
                total_value=float(row['price']) * int(row['quantity'])
            )

def filter_by_category_lazy(products: Iterable[Product], category: str) -> Iterator[Product]:
    """Lazy-фільтрація товарів за категорією."""
    return (p for p in products if p.category == category)

def apply_discount(products: Iterable[Product], discount: float) -> Iterator[Product]:
    """Lazy-трансформація: застосування знижки до ціни."""
    for p in products:
        p.price *= (1 - discount)
        p.total_value = p.price * p.quantity
        yield p

def batch_process(products: Iterable[Product], size: int) -> Generator[list[Product], None, None]:
    """Групування товарів у батчі (batching)."""
    it = iter(products)
    while True:
        batch = list(itertools.islice(it, size))
        if not batch:
            break
        yield batch

def main():
    # Симуляція великого набору даних (генератор)
    def data_source():
        for i in range(1, 21):
            yield Product(f"Product_{i}", "Electronics" if i % 2 == 0 else "Books", i * 10.0, 2, 0.0)

    print("--- Потокова обробка даних ---")
    
    # 1. Потоковий конвеєр (Lazy Pipeline)
    # Джерело -> Фільтрація -> Знижка -> Батчі
    filtered = filter_by_category_lazy(data_source(), "Electronics")
    discounted = apply_discount(filtered, 0.1)
    pipeline = batch_process(discounted, size=3)

    for i, batch in enumerate(pipeline):
        print(f"Batch {i+1}: {[p.name for p in batch]}")

if __name__ == '__main__':
    main()