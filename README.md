# Ứng dụng Phân loại 102 Loài hoa 

Một ứng dụng web demo sử dụng mô hình học sâu **Vision Transformer (ViT-B/16)** để phân loại 102 loài hoa từ bộ dữ liệu Oxford 102 Flowers. Mô hình đã được huấn luyện và tối ưu hóa để đạt độ chính xác **~91.9%** trên tập kiểm tra.



Backend của ứng dụng được xây dựng bằng **Node.js** (với kiến trúc MVC), và dịch vụ AI được cung cấp bởi một kịch bản **Python** sử dụng PyTorch.

---

## ## Tính năng Chính

* **Giao diện Đơn giản:** Giao diện web thân thiện cho phép người dùng dễ dàng tải ảnh lên.
* **Mô hình Hiệu suất cao:** Sử dụng kiến trúc `ViT-B/16` đã được tinh chỉnh sâu (fine-tuned) để cho kết quả chính xác vượt trội.
* **Kết quả Chi tiết:** Trả về Top 3 loài hoa có khả năng cao nhất cùng với phần trăm xác suất.
* **Kiến trúc Chuyên nghiệp:** Backend được tổ chức theo mô hình MVC (Model-View-Controller) để dễ dàng bảo trì và mở rộng.

---

## ## Yêu cầu Hệ thống (Prerequisites)

Trước khi bắt đầu, hãy đảm bảo máy tính của bạn đã cài đặt:

* **Node.js** (phiên bản 14.x trở lên) và **npm**.
* **Python** (phiên bản 3.9 trở lên) và **pip**.
    * **Lưu ý quan trọng:** Trong quá trình cài đặt Python trên Windows, hãy đảm bảo bạn đã **đánh dấu vào ô "Add Python to PATH"**.

---

## ## Hướng dẫn Cài đặt và Chạy

### **Bước 1: Tải Mã nguồn và File Model**

1.  **Clone repository này về máy:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```
    *(Thay `your-username/your-repository-name` bằng thông tin GitHub của bạn)*

2.  **Tải File Model:** Do file model ViT khá lớn, bạn cần tải nó về thủ công.
    * Tải file **`exp_vit.pth`** từ link sau: **[https://drive.google.com/file/d/1ACAMxI0iTu3Y8NRFKWo64lczgRPbvxif/view?usp=drive_link]**
    * Sau khi tải về, đặt file này vào đúng thư mục: `python_service/models/`.

### **Bước 2: Cài đặt Môi trường**

1.  **Cài đặt Dependencies cho Node.js:**
    Mở terminal tại thư mục gốc của dự án và chạy lệnh:
    ```bash
    npm install
    ```

2.  **Cài đặt Dependencies cho Python:**
    Vẫn trong terminal đó, chạy lệnh sau để cài đặt tất cả các thư viện AI cần thiết:
    ```bash
    pip install -r python_service/requirements.txt
    ```
    *(Quá trình này có thể mất vài phút vì cần tải về PyTorch.)*

### **Bước 3: Khởi động Ứng dụng**

1.  **Chạy server:**
    ```bash
    npm run dev
    ```
    *(Lệnh này sử dụng `nodemon` để tự động khởi động lại server khi có thay đổi code. Bạn cũng có thể dùng `npm start` để chạy bình thường.)*

2.  **Truy cập ứng dụng:**
    Mở trình duyệt web của bạn và truy cập vào địa chỉ: `http://localhost:3000`

Bây giờ bạn đã có thể tải ảnh lên và trải nghiệm mô hình phân loại hoa mạnh nhất của mình!

---

## ## Cấu trúc Dự án

Dự án được tổ chức theo kiến trúc MVC cho phần Node.js và một dịch vụ Python riêng biệt.

```
/
├── controllers/      # Logic xử lý request từ người dùng
├── models/           # Logic nghiệp vụ (gọi dịch vụ Python)
├── python_service/   # Chứa toàn bộ "bộ não" AI
│   ├── models/
│   │   └── exp_vit.pth         # File trọng số mô hình ViT
│   ├── predict.py            # Kịch bản dự đoán (đã cập nhật cho ViT)
│   └── requirements.txt      # Thư viện Python
├── public/           # Chứa các file tĩnh (ảnh upload)
│   └── uploads/
├── routes/           # Định nghĩa các URL
├── views/            # Giao diện người dùng (EJS)
├── app.js            # File server chính
└── package.json
```