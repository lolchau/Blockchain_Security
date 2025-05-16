
# 🔐 Dự án Mô phỏng Blockchain và Merkle Tree

## 📌 Mục tiêu

Dự án này nhằm mô phỏng các thành phần cốt lõi trong công nghệ Blockchain, bao gồm:

* Hàm băm mật mã (cryptographic hash function)
* Mạng lưới blockchain đơn giản
* Cấu trúc cây Merkle (Merkle Tree)
* Tích hợp hoàn chỉnh vào một hệ thống minh họa cơ bản

---

## 📁 Cấu trúc dự án

### **Phần 1: Hàm băm mật mã**

* Mục tiêu: Mô phỏng một hàm băm đơn giản tương tự SHA-256.
* Vai trò: Cung cấp nền tảng bảo mật cho các phần sau.

### **Phần 2: Mạng Blockchain cơ bản**

* Mục tiêu: Xây dựng một chuỗi khối với các block chứa dữ liệu.
* Yêu cầu: Mỗi block liên kết với block trước bằng hàm băm từ phần 1.

### **Phần 3: Cây Merkle**

* Mục tiêu: Mô phỏng cấu trúc Merkle Tree để xác minh dữ liệu giao dịch.
* Ứng dụng: Tăng hiệu quả và độ tin cậy trong việc xác thực dữ liệu trong block.

### **Phần 4: Tích hợp hoàn chỉnh**

* Mục tiêu: Kết hợp các phần trên để mô phỏng một hệ thống blockchain hoàn chỉnh với xác minh bằng Merkle Tree.

---

## 👥 Quy tắc làm việc nhóm

* Mỗi thành viên **phải tạo một nhánh (branch)** riêng theo cú pháp:

  ```
  <ten-thanh-vien>/<ten-chuc-nang>
  ```

  Ví dụ: `an/hash-function`, `linh/merkle-tree`

* **Không commit trực tiếp vào nhánh chính (main)**. Sử dụng Pull Request (PR) để xin merge sau khi hoàn tất chức năng.

* Tất cả các phần code nên được:

  * Viết rõ ràng, dễ hiểu
  * Có bình luận (comment) mô tả từng phần quan trọng
  * Kèm theo ví dụ chạy thử nếu có thể

---

## 🚀 Hướng dẫn chạy thử

```bash
# Clone repo
git clone https://github.com/lolchau/blockchain_Security.git

# Cài đặt môi trường nếu cần (Python ví dụ)
pip install -r requirements.txt

# Chạy từng phần tương ứng
python part1_hash_function.py
python part2_blockchain.py
python part3_merkle_tree.py
python part4_full_system.py
```

---

## 📌 Ghi chú

* Vui lòng cập nhật file `README.md` nếu có thay đổi về cấu trúc hoặc hướng phát triển.
* Các tài liệu tham khảo và mô tả thuật toán nên được để trong thư mục `docs/`.

---

Nếu bạn muốn mình viết kèm `requirements.txt` hoặc cấu trúc thư mục mẫu thì cứ nói nhé!
