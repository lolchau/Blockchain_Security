import hashlib
import json
from Transaction import Transaction
# --- Các hàm tiện ích cho Cây Merkle ---
def hash_pair(hash1, hash2):
    # Đảm bảo thứ tự nhất quán để băm cặp, ví dụ: sắp xếp theo alphabet
    if hash1 < hash2:
        return hashlib.sha256((hash1 + hash2).encode()).hexdigest()
    else:
        return hashlib.sha256((hash2 + hash1).encode()).hexdigest()

def build_merkle_tree_recursive(transaction_hashes):
    if not transaction_hashes:
        return hashlib.sha256("".encode()).hexdigest() # Hash cho trường hợp không có giao dịch
    if len(transaction_hashes) == 1:
        return transaction_hashes[0]

    next_level_hashes = []
    for i in range(0, len(transaction_hashes), 2):
        hash1 = transaction_hashes[i]
        if i + 1 < len(transaction_hashes):
            hash2 = transaction_hashes[i+1]
        else:
            hash2 = hash1 # Nhân đôi nếu số lượng lẻ
        next_level_hashes.append(hash_pair(hash1, hash2))

    return build_merkle_tree_recursive(next_level_hashes)

def get_merkle_root(transactions):
    if not transactions:
        return hashlib.sha256("".encode()).hexdigest()
    transaction_hashes = [tx.get_hash() for tx in transactions]
    return build_merkle_tree_recursive(transaction_hashes)

def get_merkle_proof(target_transaction_hash, all_transaction_hashes_in_block):
    """
    Tạo Merkle proof cho một giao dịch.
    Trả về: (merkle_root_tính_toán_được, list_of_proof_hashes)
    Nếu giao dịch không tồn tại, trả về (None, [])
    """
    if not all_transaction_hashes_in_block or target_transaction_hash not in all_transaction_hashes_in_block:
        return None, []

    proof = []
    current_level_hashes = list(all_transaction_hashes_in_block)
    # Lưu trữ hash mục tiêu hiện tại khi nó được băm lên các cấp cao hơn
    current_target_hash_in_tree = target_transaction_hash

    while len(current_level_hashes) > 1:
        next_level_hashes = []
        found_in_this_level = False # Cờ để biết target_hash còn ở dạng lá/nút con ở level này không
        target_idx_this_level = -1

        try:
            target_idx_this_level = current_level_hashes.index(current_target_hash_in_tree)
            found_in_this_level = True
        except ValueError:
            # current_target_hash_in_tree đã được băm lên cấp độ cha ở vòng lặp trước,
            # giờ nó không còn là một phần tử riêng lẻ ở current_level_hashes nữa.
            # Chúng ta sẽ tiếp tục xây dựng cây lên root.
            pass

        for i in range(0, len(current_level_hashes), 2):
            hash1 = current_level_hashes[i]
            hash2 = current_level_hashes[i+1] if (i + 1) < len(current_level_hashes) else hash1
            parent_hash = hash_pair(hash1, hash2)

            if found_in_this_level:
                if i == target_idx_this_level: # hash1 là target
                    if hash1 != hash2 : # Chỉ thêm vào proof nếu có sibling thực sự
                        proof.append({'hash': hash2, 'position': 'right'})
                    current_target_hash_in_tree = parent_hash # Cập nhật target cho level tiếp theo
                elif (i + 1) == target_idx_this_level: # hash2 là target
                    proof.append({'hash': hash1, 'position': 'left'})
                    current_target_hash_in_tree = parent_hash # Cập nhật target cho level tiếp theo
            next_level_hashes.append(parent_hash)
        current_level_hashes = next_level_hashes

    # current_level_hashes[0] bây giờ là Merkle Root tính toán được từ toàn bộ giao dịch
    # và current_target_hash_in_tree cũng sẽ là root nếu target_transaction_hash có trong cây
    return current_level_hashes[0] if current_level_hashes else None, proof


def verify_merkle_proof(original_target_transaction_hash, expected_merkle_root, proof_path):
    calculated_hash = original_target_transaction_hash
    for p_node in proof_path:
        sibling_hash = p_node['hash']
        position = p_node['position']

        if position == 'right':
            calculated_hash = hash_pair(calculated_hash, sibling_hash)
        elif position == 'left':
            calculated_hash = hash_pair(sibling_hash, calculated_hash)

    return calculated_hash == expected_merkle_root
