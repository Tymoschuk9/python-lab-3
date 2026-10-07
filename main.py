import itertools
import typing
import random

# Варіант №3: Обробка потоку логів транзакцій.
# Завдання: Створити конвеєр для обробки нескінченного потоку логів (користувач, сума, статус),
# відфільтрувати успішні транзакції, збільшити суму на 10% (кешбек), 
# та вибрати лише транзакції на суму більше 500 одиниць.

class Transaction:
    def __init__(self, user_id: int, amount: float, status: str):
        self.user_id = user_id
        self.amount = amount
        self.status = status

    def __repr__(self):
        return f"Transaction(user={self.user_id}, amount={self.amount:.2f}, status='{self.status}')"

def infinite_transaction_generator() -> typing.Generator[Transaction, None, None]:
    """Генератор нескінченного потоку транзакцій."""
    statuses = ["success", "failed", "pending"]
    while True:
        yield Transaction(
            user_id=random.randint(1, 100),
            amount=round(random.uniform(10.0, 1000.0), 2),
            status=random.choice(statuses)
        )

def filter_successful(transactions: typing.Iterable[Transaction]) -> typing.Iterator[Transaction]:
    """Фільтрація лише успішних транзакцій."""
    return (t for t in transactions if t.status == "success")

def apply_cashback(transactions: typing.Iterable[Transaction]) -> typing.Iterator[Transaction]:
    """Нарахування 10% кешбеку."""
    for t in transactions:
        t.amount *= 1.10
        yield t

def filter_high_value(transactions: typing.Iterable[Transaction], min_amount: float) -> typing.Iterator[Transaction]:
    """Фільтрація транзакцій вище заданого ліміту."""
    return filter(lambda t: t.amount > min_amount, transactions)

def main():
    print("--- Потокова обробка транзакцій (Варіант №3) ---")
    
    # Створення конвеєра (Lazy Pipeline)
    raw_stream = infinite_transaction_generator()
    successful = filter_successful(raw_stream)
    with_cashback = apply_cashback(successful)
    high_value = filter_high_value(with_cashback, 500.0)
    
    # Обмеження потоку за допомогою islice
    final_stream = itertools.islice(high_value, 5)
    
    for i, transaction in enumerate(final_stream, 1):
        print(f"Обробка #{i}: {transaction}")

if __name__ == "__main__":
    main()