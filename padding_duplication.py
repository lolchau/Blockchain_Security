import hashlib

# Hàm băm SHA-256
def hash_data(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Hàm tạo Merkle Tree, in từng tầng và trả về Merkle Root
def get_merkle_root(data_list):
    # Bước 1: Tạo tầng lá
    current_level = [hash_data(item) for item in data_list]
    level_num = 0  # Đếm tầng

    print(f"Tầng {level_num} (lá):")
    for idx, h in enumerate(current_level):
        print(f"  L{idx}: {h[:10]}...")

    # Lặp đến khi còn một node duy nhất
    while len(current_level) > 1:
        # Nếu số lượng node là lẻ, nhân đôi node cuối
        if len(current_level) % 2 != 0:
            current_level.append(current_level[-1])

        # Tạo tầng tiếp theo bằng cách ghép cặp và băm
        next_level = []
        print(f"\nTầng {level_num + 1}:")
        for i in range(0, len(current_level), 2):
            combined = current_level[i] + current_level[i + 1]
            combined_hash = hash_data(combined)
            next_level.append(combined_hash)
            print(f"  H({i},{i+1}): H({current_level[i][:8]}..., {current_level[i+1][:8]}...) → {combined_hash[:10]}...")

        current_level = next_level
        level_num += 1

    print(f"\nMerkle Root (Tầng {level_num}): {current_level[0]}")
    return current_level[0]

# Ví dụ
D = ["D1", "D2", "D3", "D4", "D5"]
root = get_merkle_root(D)
