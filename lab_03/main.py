import itertools
import random
from typing import Generator, Iterable, Any

# Варіант №3: Аналіз транзакцій. 
# Створити генератор для читання лог-файлу транзакцій, 
# відфільтрувати лише успішні (status="success"), 
# вирахувати податок 20% (якщо сума > 1000), 
# згрупувати за типом валюти та вивести суму транзакцій по кожній валюті.

def generate_mock_data(n: int = 100) -> Generator[str, None, None]:
    """Генератор, що емулює читання великого файлу з транзакціями."""
    currencies = ["USD", "EUR", "UAH"]
    statuses = ["success", "failed", "pending"]
    for _ in range(n):
        amount = random.randint(10, 5000)
        currency = random.choice(currencies)
        status = random.choice(statuses)
        yield f"{amount},{currency},{status}"

def stream_reader(source: Iterable[str]) -> Generator[dict, None, None]:
    """Парсинг рядків у словники."""
    for line in source:
        parts = line.strip().split(',')
        if len(parts) == 3:
            yield {"amount": float(parts[0]), "currency": parts[1], "status": parts[2]}

def filter_success(data: Iterable[dict]) -> Generator[dict, None, None]:
    """Фільтрація лише успішних транзакцій."""
    yield from (item for item in data if item["status"] == "success")

def apply_tax(data: Iterable[dict]) -> Generator[dict, None, None]:
    """Розрахунок податку 20% для транзакцій > 1000."""
    for item in data:
        if item["amount"] > 1000:
            item["amount"] *= 0.8  # Залишок після податку
        yield item

def main():
    # Джерело: емуляція потоку даних
    raw_data = generate_mock_data(50)
    
    # Lazy Pipeline
    parsed = stream_reader(raw_data)
    successful = filter_success(parsed)
    processed = apply_tax(successful)
    
    # Для групування нам потрібно відсортувати дані за валютою
    # Оскільки ми хочемо зберегти lazy evaluation, ми використовуємо список лише для сортування
    # В реальних умовах для великих файлів дані мають бути попередньо відсортовані у зовнішньому файлі
    sorted_data = sorted(processed, key=lambda x: x["currency"])
    
    print("Результати обробки транзакцій (Сума після податку за валютою):")
    for currency, group in itertools.groupby(sorted_data, key=lambda x: x["currency"]):
        total = sum(item["amount"] for item in group)
        print(f"Валюта {currency}: {total:.2f}")

if __name__ == "__main__":
    main()