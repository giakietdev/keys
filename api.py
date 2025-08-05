import os
import json
import random
import string
import subprocess
import datetime
from pathlib import Path

class APIKeyManager:
    def __init__(self, api_dir="api"):
        self.api_dir = api_dir
        self.api_folders = [
            "avatar", "joiner", "nhaydis", "nhayzalo", 
            "rename", "spamdis", "spamzalo", "voice"
        ]
    
    def generate_key(self, length=10):
        """Tạo key ngẫu nhiên"""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def get_api_folders(self):
        """Lấy danh sách các thư mục API"""
        return [folder for folder in self.api_folders if os.path.exists(os.path.join(self.api_dir, folder))]
    
    def read_keys(self, folder_name):
        """Đọc keys từ file key.txt"""
        key_file = os.path.join(self.api_dir, folder_name, "key.txt")
        if os.path.exists(key_file):
            with open(key_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []
    
    def write_keys(self, folder_name, keys):
        """Ghi keys vào file key.txt"""
        key_file = os.path.join(self.api_dir, folder_name, "key.txt")
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        with open(key_file, 'w', encoding='utf-8') as f:
            for key in keys:
                f.write(key + '\n')
    
    def add_key(self, folder_name, key=None):
        """Thêm key mới vào folder"""
        if key is None:
            key = self.generate_key()
        
        keys = self.read_keys(folder_name)
        if key not in keys:
            keys.append(key)
            self.write_keys(folder_name, keys)
            print(f"✅ Đã thêm key '{key}' vào {folder_name}")
            return key
        else:
            print(f"❌ Key '{key}' đã tồn tại trong {folder_name}")
            return None
    
    def remove_key(self, folder_name, key):
        """Xóa key khỏi folder"""
        keys = self.read_keys(folder_name)
        if key in keys:
            keys.remove(key)
            self.write_keys(folder_name, keys)
            print(f"✅ Đã xóa key '{key}' khỏi {folder_name}")
            return True
        else:
            print(f"❌ Key '{key}' không tồn tại trong {folder_name}")
            return False
    
    def list_keys(self, folder_name):
        """Liệt kê tất cả keys trong folder"""
        keys = self.read_keys(folder_name)
        print(f"\n📁 Keys trong {folder_name}:")
        for i, key in enumerate(keys, 1):
            print(f"  {i}. {key}")
        return keys
    
    def update_version(self, folder_name, version=None):
        """Cập nhật version.json"""
        version_file = os.path.join(self.api_dir, folder_name, "version.json")
        if os.path.exists(version_file):
            with open(version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {
                "version": "1.0",
                "release_date": "",
                "author": "Hoang Gia Kiet",
                "changelog": "update"
            }
        
        if version:
            data["version"] = version
        data["release_date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Đã cập nhật version cho {folder_name}")
    
    def git_operations(self):
        """Thực hiện các thao tác Git"""
        try:
            # Kiểm tra trạng thái Git
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Không phải là Git repository")
                return False
            
            # Thêm tất cả thay đổi
            subprocess.run(['git', 'add', '.'], check=True)
            print("✅ Đã add tất cả thay đổi")
            
            # Commit với message
            commit_message = f"Update API keys - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print("✅ Đã commit thay đổi")
            
            # Push lên GitHub
            subprocess.run(['git', 'push'], check=True)
            print("✅ Đã push lên GitHub")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi Git: {e}")
            return False
        except FileNotFoundError:
            print("❌ Git không được cài đặt hoặc không có trong PATH")
            return False
    
    def auto_generate_keys(self, count=1):
        """Tự động tạo keys cho tất cả folders"""
        print(f"🔄 Đang tạo {count} key(s) cho tất cả folders...")
        
        for folder in self.get_api_folders():
            print(f"\n📁 Xử lý folder: {folder}")
            for i in range(count):
                new_key = self.add_key(folder)
                if new_key:
                    self.update_version(folder)
        
        print("\n✅ Hoàn thành tạo keys!")
    
    def interactive_menu(self):
        """Menu tương tác"""
        while True:
            print("\n" + "="*50)
            print("🔑 API KEY MANAGER")
            print("="*50)
            print("1. Tạo key mới")
            print("2. Xóa key")
            print("3. Xem danh sách keys")
            print("4. Tự động tạo keys cho tất cả folders")
            print("5. Đẩy lên GitHub")
            print("6. Thoát")
            print("="*50)
            
            choice = input("Chọn chức năng (1-6): ").strip()
            
            if choice == "1":
                self.add_key_menu()
            elif choice == "2":
                self.remove_key_menu()
            elif choice == "3":
                self.list_keys_menu()
            elif choice == "4":
                count = input("Số lượng keys cần tạo cho mỗi folder: ").strip()
                try:
                    count = int(count)
                    self.auto_generate_keys(count)
                except ValueError:
                    print("❌ Vui lòng nhập số hợp lệ")
            elif choice == "5":
                self.git_operations()
            elif choice == "6":
                print("👋 Tạm biệt!")
                break
            else:
                print("❌ Lựa chọn không hợp lệ")
    
    def add_key_menu(self):
        """Menu thêm key"""
        print("\n📁 Các folders có sẵn:")
        folders = self.get_api_folders()
        for i, folder in enumerate(folders, 1):
            print(f"  {i}. {folder}")
        
        try:
            folder_idx = int(input("Chọn folder (số): ")) - 1
            if 0 <= folder_idx < len(folders):
                folder_name = folders[folder_idx]
                custom_key = input("Nhập key (để trống để tạo tự động): ").strip()
                key = custom_key if custom_key else None
                self.add_key(folder_name, key)
                self.update_version(folder_name)
            else:
                print("❌ Lựa chọn không hợp lệ")
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ")
    
    def remove_key_menu(self):
        """Menu xóa key"""
        print("\n📁 Các folders có sẵn:")
        folders = self.get_api_folders()
        for i, folder in enumerate(folders, 1):
            print(f"  {i}. {folder}")
        
        try:
            folder_idx = int(input("Chọn folder (số): ")) - 1
            if 0 <= folder_idx < len(folders):
                folder_name = folders[folder_idx]
                keys = self.read_keys(folder_name)
                if keys:
                    print(f"\nKeys trong {folder_name}:")
                    for i, key in enumerate(keys, 1):
                        print(f"  {i}. {key}")
                    
                    key_idx = int(input("Chọn key để xóa (số): ")) - 1
                    if 0 <= key_idx < len(keys):
                        key_to_remove = keys[key_idx]
                        if self.remove_key(folder_name, key_to_remove):
                            self.update_version(folder_name)
                    else:
                        print("❌ Lựa chọn không hợp lệ")
                else:
                    print(f"❌ Không có keys trong {folder_name}")
            else:
                print("❌ Lựa chọn không hợp lệ")
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ")
    
    def list_keys_menu(self):
        """Menu xem danh sách keys"""
        print("\n📁 Các folders có sẵn:")
        folders = self.get_api_folders()
        for i, folder in enumerate(folders, 1):
            print(f"  {i}. {folder}")
        print(f"  {len(folders) + 1}. Tất cả")
        
        try:
            choice = int(input("Chọn folder (số): "))
            if 1 <= choice <= len(folders):
                folder_name = folders[choice - 1]
                self.list_keys(folder_name)
            elif choice == len(folders) + 1:
                for folder in folders:
                    self.list_keys(folder)
            else:
                print("❌ Lựa chọn không hợp lệ")
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ")

def main():
    """Hàm chính"""
    manager = APIKeyManager()
    
    print("🚀 Khởi động API Key Manager...")
    print(f"📁 Tìm thấy {len(manager.get_api_folders())} API folders")
    
    # Kiểm tra Git repository
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Đã kết nối với Git repository")
        else:
            print("⚠️  Không phải là Git repository hoặc chưa khởi tạo")
    except:
        print("⚠️  Git không được cài đặt")
    
    manager.interactive_menu()

if __name__ == "__main__":
    main()
