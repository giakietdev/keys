# 🔑 API Key Manager

Script Python để tự động quản lý keys trong các thư mục API và đẩy lên GitHub.

## 📁 Cấu trúc dự án

```
keyy/
├── api/
│   ├── avatar/
│   │   ├── key.txt
│   │   └── version.json
│   ├── joiner/
│   ├── nhaydis/
│   ├── nhayzalo/
│   ├── rename/
│   ├── spamdis/
│   ├── spamzalo/
│   └── voice/
├── api.py
└── README.md
```

## 🚀 Cách sử dụng

### 1. Chạy script
```bash
python api.py
```

### 2. Menu chính
Script sẽ hiển thị menu với các tùy chọn:

- **1. Tạo key mới**: Thêm key vào một folder cụ thể
- **2. Xóa key**: Xóa key khỏi folder
- **3. Xem danh sách keys**: Liệt kê tất cả keys trong folder
- **4. Tự động tạo keys**: Tạo keys cho tất cả folders cùng lúc
- **5. Đẩy lên GitHub**: Commit và push thay đổi lên GitHub
- **6. Thoát**: Kết thúc chương trình

## 🔧 Tính năng

### Tạo key tự động
- Tạo key ngẫu nhiên với độ dài 10 ký tự
- Hỗ trợ tạo key tùy chỉnh
- Tránh trùng lặp keys

### Quản lý version
- Tự động cập nhật `version.json`
- Cập nhật ngày release
- Giữ nguyên thông tin author

### Git Integration
- Tự động add tất cả thay đổi
- Commit với timestamp
- Push lên GitHub

## 📋 Yêu cầu hệ thống

- Python 3.6+
- Git được cài đặt và cấu hình
- Quyền truy cập vào GitHub repository

## ⚙️ Cấu hình Git

Trước khi sử dụng, đảm bảo:

1. **Khởi tạo Git repository**:
```bash
git init
git remote add origin <your-github-repo-url>
```

2. **Cấu hình Git credentials**:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 🔄 Workflow

1. Chạy script: `python api.py`
2. Chọn chức năng cần thiết
3. Thực hiện thao tác (tạo/xóa key)
4. Chọn "Đẩy lên GitHub" để commit và push
5. Kiểm tra thay đổi trên GitHub

## 📝 Ví dụ sử dụng

### Tạo key mới
```
Chọn chức năng (1-6): 1
📁 Các folders có sẵn:
  1. avatar
  2. joiner
  3. nhaydis
  ...
Chọn folder (số): 1
Nhập key (để trống để tạo tự động): 
✅ Đã thêm key 'aB3xK9mN2p' vào avatar
✅ Đã cập nhật version cho avatar
```

### Tự động tạo keys cho tất cả folders
```
Chọn chức năng (1-6): 4
Số lượng keys cần tạo cho mỗi folder: 2
🔄 Đang tạo 2 key(s) cho tất cả folders...
📁 Xử lý folder: avatar
✅ Đã thêm key 'xY7zK4mN8q' vào avatar
✅ Đã thêm key 'pQ2rS9tU5v' vào avatar
...
```

### Đẩy lên GitHub
```
Chọn chức năng (1-6): 5
✅ Đã add tất cả thay đổi
✅ Đã commit thay đổi
✅ Đã push lên GitHub
```

## 🛠️ Tùy chỉnh

### Thay đổi độ dài key
Trong file `api.py`, sửa hàm `generate_key()`:
```python
def generate_key(self, length=15):  # Thay đổi từ 10 thành 15
```

### Thêm folder mới
Trong class `APIKeyManager`, cập nhật `api_folders`:
```python
self.api_folders = [
    "avatar", "joiner", "nhaydis", "nhayzalo", 
    "rename", "spamdis", "spamzalo", "voice", "new_folder"
]
```

## ⚠️ Lưu ý

- Script sẽ tự động tạo thư mục nếu chưa tồn tại
- Keys được lưu trong file `key.txt` với encoding UTF-8
- Version được cập nhật tự động khi thêm/xóa key
- Đảm bảo có quyền ghi vào thư mục và repository

## 🐛 Xử lý lỗi

### Lỗi Git
- Kiểm tra Git đã được cài đặt
- Kiểm tra repository đã được khởi tạo
- Kiểm tra remote origin đã được cấu hình

### Lỗi quyền truy cập
- Kiểm tra quyền ghi vào thư mục
- Kiểm tra quyền push lên GitHub

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Python version: `python --version`
2. Git status: `git status`
3. Repository remote: `git remote -v` 