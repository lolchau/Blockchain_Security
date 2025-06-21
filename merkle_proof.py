import hashlib

# -----------------------------------
# Hàm băm SHA-256
# -----------------------------------
def hash_data(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# -----------------------------------
# Tạo Merkle Tree và trả về tất cả các tầng
# -----------------------------------
def build_merkle_tree(data_list):
    levels = []
    current_level = [hash_data(d) for d in data_list]
    levels.append(current_level)

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else current_level[i]  # nếu lẻ thì nhân đôi
            combined = hash_data(left + right)
            next_level.append(combined)
        current_level = next_level
        levels.append(current_level)

    return levels

# -----------------------------------
# Sinh Merkle Proof cho 1 phần tử (index)
# -----------------------------------
def generate_merkle_proof(levels, index):
    proof = []
    for level in levels[:-1]:
        sibling_index = index ^ 1  # lật bit cuối → index 0 <-> 1, 2 <-> 3, v.v.
        if sibling_index < len(level):
            sibling_hash = level[sibling_index]
            position = 'right' if sibling_index > index else 'left'
            proof.append((sibling_hash, position))
        index = index // 2
    return proof

# -----------------------------------
# In chi tiết quá trình xác minh Merkle Proof
# -----------------------------------
def verify_merkle_proof_verbose(data, proof, root):
    current_hash = hash_data(data)
    print(f"Khởi đầu với dữ liệu: '{data}' → H0 = {current_hash}")

    for i, (sibling_hash, position) in enumerate(proof):
        if position == 'left':
            print(f"\nBước {i + 1}: Sibling ở trái → H = H({sibling_hash[:10]}... || {current_hash[:10]}...)")
            current_hash = hash_data(sibling_hash + current_hash)
        else:
            print(f"\nBước {i + 1}: Sibling ở phải → H = H({current_hash[:10]}... || {sibling_hash[:10]}...)")
            current_hash = hash_data(current_hash + sibling_hash)
        print(f"→ Kết quả H{i+1} = {current_hash}")

    print(f"\nSo sánh với Merkle Root công khai:")
    print(f"  H cuối cùng: {current_hash}")
    print(f"  Merkle Root: {root}")

    if current_hash == root:
        print("✅ Dữ liệu là HỢP LỆ (Merkle proof đúng)")
    else:
        print("❌ Dữ liệu KHÔNG hợp lệ (Merkle proof sai)")

# -----------------------------------
# Thực thi ví dụ
# -----------------------------------
if __name__ == "__main__":
    data = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]
    leaf_index = 3  # kiểm chứng D4

    # Bước 1: Xây cây
    levels = build_merkle_tree(data)
    root = levels[-1][0]

    # Bước 2: Tạo proof
    proof = generate_merkle_proof(levels, leaf_index)

    # Bước 3: In chi tiết quá trình xác minh
    verify_merkle_proof_verbose(data[leaf_index], proof, root)
