import hashlib
import math

# Hàm băm SHA-256
def hash_data(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Hàm kiểm tra số gần nhất là lũy thừa của 2
def next_power_of_two(n):
    return 1 if n == 0 else 2**math.ceil(math.log2(n))

# Hàm tạo Merkle Tree dùng null padding
def get_merkle_root_null_padding(data_list, dummy_value="0"):
    # Bước 1: Băm từng phần tử
    current_level = [hash_data(item) for item in data_list]

    # Bước 2: Padding bằng dummy đến khi số lượng là lũy thừa của 2
    target_len = next_power_of_two(len(current_level))
    while len(current_level) < target_len:
        current_level.append(hash_data(dummy_value))  # padding bằng hash("0")

    level_num = 0
    print(f"Tầng {level_num} (lá):")
    for idx, h in enumerate(current_level):
        print(f"  L{idx}: {h[:10]}...")

    # Bước 3: Lặp cho đến khi còn 1 node duy nhất
    while len(current_level) > 1:
        next_level = []
        print(f"\nTầng {level_num + 1}:")
        for i in range(0, len(current_level), 2):
            combined = current_level[i] + current_level[i + 1]
            new_hash = hash_data(combined)
            next_level.append(new_hash)
            print(f"  H({i},{i+1}): H({current_level[i][:8]}..., {current_level[i+1][:8]}...) → {new_hash[:10]}...")

        current_level = next_level
        level_num += 1

    print(f"\nMerkle Root (Tầng {level_num}): {current_level[0]}")
    return current_level[0]

# Ví dụ sử dụng:
D = ["D1", "D2", "D3", "D4", "D5"]
root = get_merkle_root_null_padding(D)
