
from Transaction import Transaction
from Merkleroot import get_merkle_proof, verify_merkle_proof
from Block import Block
import hashlib
import time
import json
# --- Lớp Blockchain ---
class Blockchain:
    def __init__(self, difficulty=3): # Độ khó mặc định
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = difficulty
        self.miner_reward = 50 # Phần thưởng cho người đào

    def create_genesis_block(self):
        return Block(time.time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if not transaction.sender or not transaction.recipient:
            print("Lỗi: Giao dịch phải có người gửi và người nhận.")
            return False
        if transaction.amount <= 0:
            print("Lỗi: Số tiền giao dịch phải lớn hơn 0.")
            return False
        # Trong một hệ thống thực, bạn sẽ cần xác thực giao dịch kỹ hơn (ví dụ: chữ ký, số dư)
        self.pending_transactions.append(transaction)
        print(f"Giao dịch đã được thêm vào hàng chờ: {transaction}")
        return True

    def mine_pending_transactions(self, miner_reward_address):
        if not self.pending_transactions:
            print("Không có giao dịch nào đang chờ để đào.")
            return False

        print(f"\nBắt đầu đào khối mới cho {len(self.pending_transactions)} giao dịch đang chờ...")
        reward_tx = Transaction("HeThong", miner_reward_address, self.miner_reward)
        # Thêm giao dịch thưởng vào đầu danh sách giao dịch của khối mới
        block_transactions = [reward_tx] + self.pending_transactions

        new_block = Block(
            time.time(),
            block_transactions,
            self.get_latest_block().hash
        )
        new_block.mine_block(self.difficulty)

        print(f"Khối mới đã được thêm vào chuỗi.")
        self.chain.append(new_block)
        self.pending_transactions = [] # Xóa các giao dịch đã được xử lý
        return True


    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                print(f"LỖI: Hash của khối #{i} ({current_block.hash[:10]}...) không hợp lệ.")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"LỖI: Previous hash của khối #{i} không khớp với hash của khối #{i-1}.")
                return False

            # Kiểm tra Merkle Root có được tính đúng từ các giao dịch trong khối không
            expected_merkle_root = get_merkle_root(current_block.transactions)
            if current_block.merkle_root != expected_merkle_root:
                print(f"LỖI: Merkle Root của khối #{i} ({current_block.merkle_root[:10]}...) không khớp với Merkle Root được tính toán ({expected_merkle_root[:10]}...).")
                return False

        print("Blockchain hợp lệ.")
        return True

    def display_chain(self):
        print("\n--- TOÀN BỘ BLOCKCHAIN ---")
        for i, block in enumerate(self.chain):
            print(f"--- Khối #{i} (ID Khối/Hash: {block.hash}) ---")
            print(str(block))
            print("-" * 30)

    def find_and_verify_transaction(self, transaction_hash_to_check):
        """
        Tìm kiếm giao dịch trong toàn bộ blockchain và xác minh bằng Merkle Proof nếu tìm thấy.
        """
        found_in_any_block = False
        for i, block in enumerate(self.chain):
            if not block.transactions:
                continue

            all_tx_hashes_in_this_block = block.get_transaction_hashes()
            if transaction_hash_to_check in all_tx_hashes_in_this_block:
                found_in_any_block = True
                print(f"\nTìm thấy giao dịch '{transaction_hash_to_check[:10]}...' trong Khối #{i} (Hash: {block.hash[:10]}...).")
                print("Đang tiến hành xác minh bằng Merkle Proof...")

                # Lấy Merkle Proof
                # Lưu ý: get_merkle_proof trả về (calculated_root_from_all_tx, proof_path)
                # calculated_root_from_all_tx phải khớp với block.merkle_root
                _, proof = get_merkle_proof(transaction_hash_to_check, all_tx_hashes_in_this_block)

                if proof is None : # Điều này không nên xảy ra nếu đã tìm thấy hash trong all_tx_hashes_in_this_block
                    print(f"Lỗi: Không thể tạo Merkle proof cho giao dịch dù đã tìm thấy hash trong khối.")
                    continue # Kiểm tra khối tiếp theo nếu có

                is_verified = verify_merkle_proof(transaction_hash_to_check, block.merkle_root, proof)

                if is_verified:
                    print(f"XÁC MINH THÀNH CÔNG: Giao dịch '{transaction_hash_to_check[:10]}...' thực sự là một phần của Khối #{i} và Merkle Root là chính xác.")
                else:
                    print(f"XÁC MINH THẤT BẠI: Giao dịch '{transaction_hash_to_check[:10]}...' được tìm thấy trong danh sách giao dịch của Khối #{i}, "
                          f"nhưng Merkle Proof không thành công. Có thể có lỗi trong logic proof hoặc dữ liệu khối không nhất quán.")
                return # Kết thúc sau khi tìm và xác minh (giả sử giao dịch chỉ ở 1 khối)

        if not found_in_any_block:
            print(f"\nKhông tìm thấy giao dịch với hash '{transaction_hash_to_check[:10]}...' trong bất kỳ khối nào của blockchain.")
