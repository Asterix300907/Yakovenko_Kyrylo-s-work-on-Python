"""Демонстрація race condition та захист через Lock."""

import threading
import time
import random


class BankAccount:
    """Банківський рахунок без синхронізації (небезпечний)."""

    def __init__(self, balance: float = 0.0):
        self.balance = balance
        self.transaction_count = 0

    def deposit(self, amount: float) -> None:
        """Поповнення рахунку."""
        # Імітація неатомарної операції
        current = self.balance
        time.sleep(random.uniform(0.0001, 0.001))
        self.balance = current + amount
        self.transaction_count += 1

    def withdraw(self, amount: float) -> bool:
        """Зняття коштів. Повертає True, якщо операція успішна."""
        current = self.balance
        time.sleep(random.uniform(0.0001, 0.001))
        if current >= amount:
            self.balance = current - amount
            self.transaction_count += 1
            return True
        return False


class SafeBankAccount:
    """Банківський рахунок із синхронізацією через Lock."""

    def __init__(self, balance: float = 0.0):
        self.balance = balance
        self.transaction_count = 0
        self._lock = threading.Lock()

    def deposit(self, amount: float) -> None:
        """Поповнення рахунку з блокуванням."""
        with self._lock:
            current = self.balance
            time.sleep(random.uniform(0.0001, 0.001))
            self.balance = current + amount
            self.transaction_count += 1

    def withdraw(self, amount: float) -> bool:
        """Зняття коштів з блокуванням."""
        with self._lock:
            current = self.balance
            time.sleep(random.uniform(0.0001, 0.001))
            if current >= amount:
                self.balance = current - amount
                self.transaction_count += 1
                return True
            return False


def run_transactions(
    account,
    num_deposits: int,
    deposit_amount: float,
    num_withdrawals: int,
    withdraw_amount: float,
):
    """Запускає 10 потоків (5 на депозит, 5 на зняття) для виконання транзакцій."""
    threads = []
    num_threads = 10  # 5 для deposit, 5 для withdraw

    deposits_per_thread = num_deposits // (num_threads // 2)
    withdrawals_per_thread = num_withdrawals // (num_threads // 2)

    def worker_deposit():
        for _ in range(deposits_per_thread):
            account.deposit(deposit_amount)

    def worker_withdraw():
        for _ in range(withdrawals_per_thread):
            account.withdraw(withdraw_amount)

    # Створення потоків для депозитів
    for _ in range(num_threads // 2):
        t = threading.Thread(target=worker_deposit)
        threads.append(t)

    # Створення потоків для зняття
    for _ in range(num_threads // 2):
        t = threading.Thread(target=worker_withdraw)
        threads.append(t)

    # Запуск усіх потоків
    for t in threads:
        t.start()

    # Очікування завершення усіх потоків
    for t in threads:
        t.join()


def main():
    initial_balance = 1000.0
    num_deposits = 100
    deposit_amount = 50.0
    num_withdrawals = 100
    withdraw_amount = 50.0

    expected_balance = (
        initial_balance
        + num_deposits * deposit_amount
        - num_withdrawals * withdraw_amount
    )
    expected_transactions = num_deposits + num_withdrawals

    # === Тест 1: Без синхронізації ===
    print("=== Тест без синхронізації (Race Condition) ===")
    unsafe_account = BankAccount(initial_balance)
    run_transactions(
        unsafe_account, num_deposits, deposit_amount, num_withdrawals, withdraw_amount
    )
    
    print(f"Очікуваний баланс:       {expected_balance:.2f}")
    print(f"Фактичний баланс:        {unsafe_account.balance:.2f}")
    print(f"Очікувано транзакцій:    {expected_transactions}")
    print(f"Фактично транзакцій:     {unsafe_account.transaction_count}")
    
    is_correct = (
        unsafe_account.balance == expected_balance 
        and unsafe_account.transaction_count == expected_transactions
    )
    print(f"Результат: {'ВИПАДКОВИЙ УСПІХ' if is_correct else 'ПОМИЛКА (втрати даних через Race Condition)'}")

    # === Тест 2: З синхронізацією (Lock) ===
    print("\n=== Тест із синхронізацією (Lock) ===")
    safe_account = SafeBankAccount(initial_balance)
    run_transactions(
        safe_account, num_deposits, deposit_amount, num_withdrawals, withdraw_amount
    )
    
    print(f"Очікуваний баланс:       {expected_balance:.2f}")
    print(f"Фактичний баланс:        {safe_account.balance:.2f}")
    print(f"Очікувано транзакцій:    {expected_transactions}")
    print(f"Фактично транзакцій:     {safe_account.transaction_count}")
    
    is_correct_safe = (
        safe_account.balance == expected_balance 
        and safe_account.transaction_count == expected_transactions
    )
    print(f"Результат: {'УСПІХ (дані захищено)' if is_correct_safe else 'ПОМИЛКА'}")


if __name__ == "__main__":
    main()