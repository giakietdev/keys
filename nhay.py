import requests
import time
from datetime import datetime
from colorama import init, Fore, Style
from pystyle import Write, Colors

init(autoreset=True)

KEYS_DATABASE_URL = "https://raw.githubusercontent.com/giakietdev/keys/refs/heads/master/api/voice/key.txt?token=GHSAT0AAAAAADETXNK3SOXG2XEOVS7L2MGE2ER4KIA"
VERSION_URL = "https://raw.githubusercontent.com/giakietdev/keys/master/api/nhaydis/version.json"
WEBHOOK_URL = "https://discord.com/api/webhooks/1402137490915201117/om8yvptbrg_c_fZfn_WpqFYxkjVXNjFpjQ8T0VHyijb_U5v9kMfD2deu3eaUbnKvjLPU"
CACHE_DURATION = 60  
cache = {}

def prompt_for_key():
    Write.Print("[SYSTEM] Nhập key: ", Colors.green_to_white, interval=0.002)
    return input().strip()

def validate_api_key(api_key):
    if not api_key:
        Write.Print("[SYSTEM] Key không được để trống!\n", Colors.red_to_purple, interval=0.002)
        return False
    
    try:
        response = requests.get(KEYS_DATABASE_URL, timeout=10)
        response.raise_for_status()
        keys_text = response.text.strip()
        
        valid_keys = []
        for line in keys_text.split('\n'):
            key = line.strip()
            if key and not key.startswith('#'):  
                valid_keys.append(key)
        
        if api_key in valid_keys:
            Write.Print("[SYSTEM] Key hợp lệ!\n", Colors.green_to_white, interval=0.002)
            return True
        else:
            Write.Print("[SYSTEM] Key không hợp lệ!\n", Colors.red_to_purple, interval=0.002)
            return False
            
    except requests.exceptions.ConnectionError:
        Write.Print("[SYSTEM] Lỗi kết nối! Không thể kiểm tra key.\n", Colors.red_to_purple, interval=0.002)
        return False
    except Exception as e:
        Write.Print(f"[SYSTEM] Lỗi không xác định: {str(e)}\n", Colors.red_to_purple, interval=0.002)
        return False

def check_version(current_version):
    try:
        response = requests.get(VERSION_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        latest_version = data.get('version', '0.0')
        changelog_text = data.get('changelog', '')
        
        if latest_version != str(current_version):
            Write.Print(f"[SYSTEM] Có phiên bản mới: {latest_version}\n", Colors.red_to_purple, interval=0.002)
            if changelog_text:
                Write.Print(f"[SYSTEM] Changelog:\n{changelog_text}\n", Colors.cyan_to_white, interval=0.002)
        else:
            Write.Print(f"[SYSTEM] Đang sử dụng phiên bản mới nhất: {current_version}\n", Colors.green_to_white, interval=0.002)
            
    except requests.exceptions.ConnectionError:
        Write.Print("[SYSTEM] Không thể kiểm tra cập nhật do lỗi kết nối.\n", Colors.red_to_purple, interval=0.002)
    except Exception as e:
        Write.Print(f"[SYSTEM] Lỗi khi kiểm tra cập nhật: {str(e)}\n", Colors.red_to_purple, interval=0.002)

def get_ip_info():
    local_ip = "Unknown"
    public_ip = "Unknown"
    
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        pass
    
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code == 200:
            public_ip = response.text.strip()
    except:
        pass
    
    return local_ip, public_ip

def send_webhook(key, tool_name):
    try:
        local_ip, public_ip = get_ip_info()
        
        embed = {
            "title": f"🔑 {tool_name} - Key Activation",
            "color": 0x00ff00,
            "fields": [
                {
                    "name": "🔑 Key",
                    "value": f"`{key[:10]}...{key[-10:] if len(key) > 20 else key}`",
                    "inline": True
                },
                {
                    "name": "🖥️ Local IP",
                    "value": f"`{local_ip}`",
                    "inline": True
                },
                {
                    "name": "🌐 Public IP",
                    "value": f"`{public_ip}`",
                    "inline": True
                },
                {
                    "name": "⏰ Timestamp",
                    "value": f"<t:{int(time.time())}:F>",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Nhây Discord Tool - Made by Hoang Gia Kiet"
            },
            "timestamp": datetime.now(datetime.UTC).isoformat()
        }
        
        payload = {
            "embeds": [embed]
        }
        
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        pass

def tai_keys_database():
    global cache
    current_time = time.time()
    if KEYS_DATABASE_URL in cache:
        cached_data, timestamp = cache[KEYS_DATABASE_URL]
        if current_time - timestamp < CACHE_DURATION:
            return cached_data

    try:
        response = requests.get(KEYS_DATABASE_URL)
        response.raise_for_status()
        keys_text = response.text.strip()
        keys_list = []
        for line in keys_text.split('\n'):
            key = line.strip()
            if key and not key.startswith('#'):  
                keys_list.append(key)
        

        cache[KEYS_DATABASE_URL] = (keys_list, current_time)
        return keys_list
    except (requests.RequestException, Exception) as e:
        Write.Print(f"[SYSTEM] Lỗi khi tải hoặc phân tích key file: {str(e)}\n", Colors.red_to_white, interval=0.002)
        return None

def kiem_tra_khoa(khoa):
    data = tai_keys_database()
    if data is None:
        return False

    if khoa not in data:
        return False

    return True

api_key = prompt_for_key()
if not validate_api_key(api_key):
    Write.Print("[SYSTEM] Key không hợp lệ, thoát chương trình...\n", Colors.red_to_purple, interval=0.002)
    exit()

send_webhook(api_key, "Nhây Tool")

check_version(2.4)

Write.Print("[SYSTEM] Key hợp lệ, tiếp tục chương trình...\n", Colors.green_to_white, interval=0.002)

import threading
import requests
import time
import os
from colorama import init
from pystyle import Colors, Colorate
from datetime import datetime
import locale
import random
VERSION = 2.4
init(autoreset=True)
lock = threading.Lock()
sent_messages = 0

try:
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, '')

def get_time():
    return datetime.now().strftime("%A | %H:%M:%S | %d/%m/%Y")

def get_banner():
    return Colorate.Diagonal(Colors.green_to_white, f"""
███╗   ██╗██╗  ██╗ █████╗ ██╗   ██╗██████╗ ██╗   ██╗
████╗  ██║██║  ██║██╔══██╗╚██╗ ██╔╝██╔══██╗╚██╗ ██╔╝
██╔██╗ ██║███████║███████║ ╚████╔╝ ██████╔╝ ╚████╔╝ 
██║╚██╗██║██╔══██║██╔══██║  ╚██╔╝  ██╔═══╝   ╚██╔╝  
██║ ╚████║██║  ██║██║  ██║   ██║██╗██║        ██║   
╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝╚═╝╚═╝        ╚═╝   
Nhây Discord Version 2.4 Made By Hoang Gia Kiet | {get_time()}
""")

def log_info(msg): 
    print(Colorate.Horizontal(Colors.green_to_white, f"[SYSTEM] {msg}"))

def log_success(msg): 
    print(Colorate.Horizontal(Colors.green_to_white, f"[SYSTEM] {msg}"))

def log_warning(msg): 
    print(Colorate.Horizontal(Colors.green_to_white, f"[SYSTEM] {msg}"))

def log_input(msg): 
    return input(Colorate.Horizontal(Colors.green_to_white, f"[INPUT] {msg}"))

def log_message(channel_id, content, token):
    global sent_messages
    short_token = f"{token[:6]}...{token[-6:]}"
    print(Colorate.Horizontal(Colors.green_to_white, 
        f"[HANGGING] | Token: {short_token} | ID Chanel: {channel_id} | Status: Sucessfully | Quantity: {sent_messages}"
    ))

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"\n{get_banner()}")
    print(Colorate.Horizontal(Colors.green_to_white, "═" * 80))

def read_tokens(file_name):
    if not os.path.exists(file_name):
        log_warning(f"File '{file_name}' không tồn tại!")
        return []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            tokens = [line.strip() for line in f if line.strip()]
            log_success(f"Tải {len(tokens)} token từ '{file_name}'")
            return tokens
    except Exception as e:
        log_warning(f"Lỗi khi đọc file '{file_name}': {str(e)}")
        return []

def get_user_input():
    clear_screen()
    log_info("Setting Tool Nhây...")

    log_info("Chọn chế độ token:")
    log_info("1. Đơn token (Nhây 1 token, 1 Channel)")
    log_info("2. Đa token (Nhây đa token, đa Channel)")
    token_mode = log_input("Nhập lựa chọn (1 hoặc 2): ")
    while token_mode not in ["1", "2"]:
        log_warning("Lựa chọn phải là 1 hoặc 2!")
        token_mode = log_input("Nhập lựa chọn (1 hoặc 2): ")

    config = {
        "token_mode": "single" if token_mode == "1" else "multi",
        "discord": {"channel_ids": []},
        "delay": 1.0,
        "tag_users": False,
        "user_ids": [],
        "use_typing": True,
        "typing_delay_min": 0.3,
        "typing_delay_max": 0.5
    }

    if token_mode == "1":  
        token = log_input("Nhập token Discord: ").strip()
        if not token:
            log_warning("Token không được để trống!")
            input(Colorate.Horizontal(Colors.green_to_white, "[EXIT] Nhấn Enter để thoát..."))
            exit(1)
        config["single_token"] = token

        channel_id = log_input("Nhập ID Channel: ").strip()
        if not channel_id.isdigit():
            log_warning("ID channel phải là số!")
            input(Colorate.Horizontal(Colors.green_to_white, "[EXIT] Nhấn Enter để thoát..."))
            exit(1)
        config["discord"]["channel_ids"] = [channel_id]
        log_success(f"Đã chọn channel: {channel_id}")
    else:  
        token_file = log_input("Nhập file chứa token: ").strip()
        if not token_file:
            log_warning("Tên file không được để trống!")
            input(Colorate.Horizontal(Colors.green_to_white, "[EXIT] Nhấn Enter để thoát..."))
            exit(1)
        config["token_file"] = token_file

        log_info("Nhập ID Channel (nhập 'gk' để dừng):")
        while True:
            channel_id = log_input("Channel ID: ").strip()
            if channel_id.lower() == "gk":
                if not config["discord"]["channel_ids"]:
                    log_warning("Cần ít nhất 1 id channel!")
                    continue
                break
            if channel_id.isdigit():
                config["discord"]["channel_ids"].append(channel_id)
                log_success(f"Thêm channel: {channel_id}")
            else:
                log_warning("ID kênh phải là số!")


    default_delay = "1.0"
    log_info("Cấu hình Delay:")
    while True:
        delay_input = log_input(f"Nhập Delay [mặc định: {default_delay}]: ") or default_delay
        try:
            delay = float(delay_input)
            if delay >= 0:
                config["delay"] = delay
                log_success(f"Delay: {delay}s")
                break
            log_warning("Delay phải >= 0!")
        except ValueError:
            log_warning("Delay phải là số!")

    log_info("Tag người dùng:")
    log_info("y: Có")
    log_info("n: Không")
    tag_choice = log_input("Nhập lựa chọn (y/n) [mặc định: n]: ").lower() or "n"
    config["tag_users"] = tag_choice == "y"
    if config["tag_users"]:
        log_info("Nhập ID người dùng (nhập 'gk' để dừng):")
        while True:
            user_id = log_input("ID: ")
            if user_id.strip().lower() == "gk":
                break
            if user_id.isdigit():
                config["user_ids"].append(user_id)
                log_success(f"Thêm ID: {user_id}")
            else:
                log_warning("ID người dùng phải là số!")

    log_info("Bật Fake Typing?")
    log_info("y: Có ")
    log_info("n: Không")
    typing_choice = log_input("Nhập lựa chọn (y/n) [mặc định: y]: ").lower() or "y"
    config["use_typing"] = typing_choice == "y"
    if not config["use_typing"]:
        config["typing_delay_min"] = 0.0
        config["typing_delay_max"] = 0.0
        log_success("Tắt fake typing")
    else:
        log_success("Bật fake typing ")

    content_file = log_input("Nhập file chứa nội dung: ").strip()
    if not content_file or not os.path.exists(content_file):
        log_warning(f"File '{content_file}' không tồn tại hoặc tên file trống!")
        input(Colorate.Horizontal(Colors.green_to_white, "[EXIT] Nhấn Enter để thoát..."))
        exit(1)
    config["content_file"] = content_file
    log_success(f"Đã chọn file nội dung: {content_file}")

    return config

def nhay_datoken_thread(token_idx, all_tokens, channel_id, messages, start_index, delay, tags=None, use_typing=False, typing_delay_min=0.3, typing_delay_max=0.5):
    global sent_messages
    total_tokens = len(all_tokens)
    index = start_index
    while True:
        token = all_tokens[token_idx % total_tokens]
        try:
            headers = {"Authorization": token, "Content-Type": "application/json"}
            if use_typing:
                requests.post(f"https://discord.com/api/v9/channels/{channel_id}/typing", headers=headers)
                time.sleep(random.uniform(typing_delay_min, typing_delay_max))
            start_time = time.time()
            content = messages[index % len(messages)]
            if tags:
                content = f"{content} {' '.join(tags)}"
            payload = {"content": content}
            response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload)
            if response.status_code == 429:
                time.sleep(2)
                continue
            if response.status_code == 200:
                with lock:
                    sent_messages += 1
                    log_message(channel_id, content, token)
            index += total_tokens
            elapsed_time = time.time() - start_time
            remaining_delay = max(0, delay - elapsed_time)
            time.sleep(remaining_delay)
        except:
            time.sleep(2)

def main():
    config = get_user_input()
    if config["token_mode"] == "single":
        tokens = [config["single_token"]]
    else:
        tokens = read_tokens(config["token_file"])
        if not tokens:
            log_warning("Không có token hợp lệ trong file!")
            input(Colorate.Horizontal(Colors.green_to_white, "[EXIT] Nhấn Enter để thoát..."))
            return

    try:
        with open(config["content_file"], "r", encoding="utf-8") as f:
            messages = [line.strip() for line in f if line.strip()]
        if not messages:
            log_warning("File nội dung rỗng!")
            input(Colorate.Horizontal(Colors.green_to_white, "[EXIT] Nhấn Enter để thoát..."))
            return
    except FileNotFoundError:
        log_warning(f"Không tìm thấy file '{config['content_file']}'!")
        input(Colorate.Horizontal(Colors.green_to_white, "[EXIT] Nhấn Enter để thoát..."))
        return

    threads = []
    total_threads = 0
    clear_screen()
    tags = [f"<@{uid}>" for uid in config["user_ids"]] if config["tag_users"] and config["user_ids"] else None
    for channel_id in config["discord"]["channel_ids"]:
        for i in range(len(tokens)):
            thread = threading.Thread(
                target=nhay_datoken_thread,
                args=(i, tokens, channel_id, messages, i, config["delay"], tags, config["use_typing"], config["typing_delay_min"], config["typing_delay_max"]),
                daemon=True
            )
            threads.append(thread)
            thread.start()
            total_threads += 1

    log_success(f"Đang khởi động {total_threads} luồng...")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
