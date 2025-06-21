import hashlib
import math

# Hàm băm SHA-256
def hash_data(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Thuật toán xây Merkle Tree kiểu Monero (không padding)
def monero_merkle_tree(data_list):
    # Băm tất cả các phần tử
    leaf = [hash_data(d) for d in data_list]
    n = len(leaf)
    if n == 1:
        print("Merkle Root:", leaf[0])
        return leaf[0]

    # Bước 1: Tính x, m = 2^x, r = m - n
    x = math.ceil(math.log2(n))
    m = 2 ** x
    r = m - n
    print(f"Số phần tử n = {n}, x = {x}, m = {m}, r = {r}")

    # Bước 2: Lần lặp đầu tiên (special)
    level1 = []

    print("\nTầng 0 (lá):")
    for i, h in enumerate(leaf):
        print(f"  L{i}: {h[:10]}...")

    # Giữ nguyên các nút từ 0 đến r-1
    for i in range(r):
        level1.append(leaf[i])

    # Ghép các cặp còn lại bắt đầu từ r
    print("\nGhép đặc biệt (r → n-1):")
    for i in range(r, n - 1, 2):
        combined = leaf[i] + leaf[i + 1]
        hashed = hash_data(combined)
        level1.append(hashed)
        print(f"  H({i},{i+1}): H({leaf[i][:8]}..., {leaf[i+1][:8]}...) → {hashed[:10]}...")

    # Bước 3: Các tầng tiếp theo (Merkle chuẩn)
    level_num = 1
    curr = level1
    while len(curr) > 1:
        next_level = []
        print(f"\nTầng {level_num}:")
        for j in range(0, len(curr), 2):
            combined = curr[j] + curr[j + 1]
            hashed = hash_data(combined)
            next_level.append(hashed)
            print(f"  H({j},{j+1}): H({curr[j][:8]}..., {curr[j+1][:8]}...) → {hashed[:10]}...")
        curr = next_level
        level_num += 1

    print(f"\nMerkle Root (Tầng {level_num}): {curr[0]}")
    return curr[0]

# ✅ Ví dụ
D = ["D1", "D2", "D3", "D4", "D5"]
root = monero_merkle_tree(D)
