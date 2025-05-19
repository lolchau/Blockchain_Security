from Blockchain import Blockchain
from Transaction import Transaction
from Merkleroot import get_merkle_proof, verify_merkle_proof

# --- Giao diện người dùng tương tác ---
if __name__ == "__main__":
    # Khởi tạo blockchain với độ khó (ví dụ: 3 hoặc 4 để thấy việc đào)
    # Độ khó 4 có thể mất chút thời gian
    try:
        difficulty_level = int(input("Nhập độ khó cho việc đào khối (ví dụ: 2, 3, 4): "))
        if difficulty_level < 1: difficulty_level = 2
    except ValueError:
        print("Độ khó không hợp lệ, sử dụng giá trị mặc định là 2.")
        difficulty_level = 2

    my_blockchain = Blockchain(difficulty=difficulty_level)
    print(f"\nBlockchain đã được khởi tạo với độ khó = {my_blockchain.difficulty}.")
    print("Khối nguyên thủy đã được tạo:")
    print(f"--- Khối #0 (ID Khối/Hash: {my_blockchain.chain[0].hash}) ---")
    print(str(my_blockchain.chain[0]))
    print("-" * 30)


    while True:
        print("\nChọn một hành động:")
        print("1. Thêm giao dịch mới")
        print("2. Đào khối (xử lý các giao dịch đang chờ)")
        print("3. Hiển thị toàn bộ Blockchain")
        print("4. Kiểm tra tính hợp lệ của Blockchain")
        print("5. Tìm và xác minh một giao dịch (bằng hash)")
        print("6. Thoát")

        choice = input("Lựa chọn của bạn: ")

        if choice == '1':
            print("\n--- Thêm giao dịch mới ---")
            sender = input("Nhập tên người gửi: ")
            recipient = input("Nhập tên người nhận: ")
            try:
                amount = float(input("Nhập số tiền: "))
                if amount <= 0:
                    print("Số tiền phải là một số dương.")
                    continue
                tx = Transaction(sender, recipient, amount)
                my_blockchain.add_transaction(tx)
                print(f"Hash của giao dịch vừa tạo: {tx.get_hash()}")
            except ValueError:
                print("Số tiền không hợp lệ. Vui lòng nhập một số.")

        elif choice == '2':
            if not my_blockchain.pending_transactions:
                print("\nKhông có giao dịch nào đang chờ để đào.")
            else:
                miner_address = input("\nNhập địa chỉ của người đào để nhận thưởng: ")
                my_blockchain.mine_pending_transactions(miner_address)

        elif choice == '3':
            my_blockchain.display_chain()

        elif choice == '4':
            print("\n--- Kiểm tra tính hợp lệ của Blockchain ---")
            my_blockchain.is_chain_valid()

        elif choice == '5':
            print("\n--- Tìm và xác minh giao dịch ---")
            tx_hash_to_verify = input("Nhập hash của giao dịch bạn muốn kiểm tra: ").strip()
            if len(tx_hash_to_verify) != 64: # SHA256 hash length
                 print("Hash giao dịch không hợp lệ. Hash phải có độ dài 64 ký tự hexa.")
                 continue
            my_blockchain.find_and_verify_transaction(tx_hash_to_verify)

        elif choice == '6':
            print("Đang thoát chương trình...")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")