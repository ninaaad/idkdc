import threading
import time

class LamportClock:
    def __init__(self):
        self.clock = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.clock += 1
            return self.clock

    def update(self, received_clock):
        with self.lock:
            self.clock = max(self.clock, received_clock) + 1
            return self.clock

class Account:
    def __init__(self, account_id, initial_balance=0):
        self.account_id = account_id
        self.balance = initial_balance
        self.lock = threading.Lock()

    def debit(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False

    def credit(self, amount):
        with self.lock:
            self.balance += amount

class Bank:
    def __init__(self):
        self.accounts = {}
        self.clock = LamportClock()
        self.transactions = []

    def add_account(self, account_id, initial_balance=0):
        self.accounts[account_id] = Account(account_id, initial_balance)

    def transfer(self, from_id, to_id, amount):
        if from_id not in self.accounts or to_id not in self.accounts:
            print(f"Invalid accounts: {from_id} or {to_id}")
            return

        from_account = self.accounts[from_id]
        to_account = self.accounts[to_id]

        # Get timestamp for debit
        debit_timestamp = self.clock.increment()

        # Process debit
        if not from_account.debit(amount):
            print(f"Insufficient funds in account {from_id}")
            return

        # Get timestamp for credit (after debit)
        credit_timestamp = self.clock.increment()

        # Process credit
        to_account.credit(amount)

        # Record transaction
        transaction = {
            'from': from_id,
            'to': to_id,
            'amount': amount,
            'debit_timestamp': debit_timestamp,
            'credit_timestamp': credit_timestamp
        }
        self.transactions.append(transaction)

        print(f"Transfer successful: {from_id} -> {to_id} ${amount}, Debit TS: {debit_timestamp}, Credit TS: {credit_timestamp}")

    def print_balances(self):
        print("\nAccount Balances:")
        for acc_id, acc in self.accounts.items():
            print(f"Account {acc_id}: ${acc.balance}")

    def print_transactions(self):
        print("\nTransactions:")
        for tx in self.transactions:
            print(f"{tx['from']} -> {tx['to']} ${tx['amount']}, Debit TS: {tx['debit_timestamp']}, Credit TS: {tx['credit_timestamp']}")

def simulate_transfers(bank):
    # Simulate concurrent transfers
    transfers = [
        (1, 2, 100),
        (2, 3, 50),
        (3, 1, 75),
        (1, 2, 25),
        (2, 3, 30)
    ]

    threads = []
    for from_id, to_id, amount in transfers:
        t = threading.Thread(target=bank.transfer, args=(from_id, to_id, amount))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def main():
    bank = Bank()
    bank.add_account(1, 1000)
    bank.add_account(2, 500)
    bank.add_account(3, 300)

    print("Initial balances:")
    bank.print_balances()

    simulate_transfers(bank)

    print("\nFinal balances:")
    bank.print_balances()

    bank.print_transactions()

    # Verify timestamps: debit < credit for each transaction
    print("\nVerifying Lamport clock order:")
    for tx in bank.transactions:
        if tx['debit_timestamp'] < tx['credit_timestamp']:
            print(f"Transaction {tx['from']}->{tx['to']}: Debit TS {tx['debit_timestamp']} < Credit TS {tx['credit_timestamp']} ✓")
        else:
            print(f"ERROR: Debit TS {tx['debit_timestamp']} >= Credit TS {tx['credit_timestamp']}")

if __name__ == "__main__":
    main()
