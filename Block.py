import hashlib
import time
import json
from Merkleroot import get_merkle_root
from Transaction import Transaction
# --- Lớp Block ---
class Block:
    def __init__(self, timestamp, transactions, previous_hash=''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.merkle_root = get_merkle_root(transactions)
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_contents = (
            str(self.timestamp)
            + str(self.merkle_root)
            + str(self.previous_hash)
            + str(self.nonce)
        )
        return hashlib.sha256(block_contents.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        start_time = time.time()
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        end_time = time.time()
        print(f"Khối đã được đào thành công: {self.hash} (trong {end_time - start_time:.2f} giây, nonce: {self.nonce})")


    def __str__(self):
        transactions_str = "\n      ".join([str(tx) for tx in self.transactions])
        return (f"  Timestamp: {time.ctime(self.timestamp)}\n"
                f"  Hash: {self.hash}\n"
                f"  Merkle Root: {self.merkle_root}\n"
                f"  Previous Hash: {self.previous_hash}\n"
                f"  Nonce: {self.nonce}\n"
                f"  Số lượng giao dịch: {len(self.transactions)}\n"
                f"  Giao dịch:\n      {transactions_str if self.transactions else 'Không có giao dịch'}")

    def get_transaction_hashes(self):
        return [tx.get_hash() for tx in self.transactions]