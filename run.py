#!/usr/bin/env python3
"""
Script đơn giản để quản lý API keys
Sử dụng: python run.py [command] [options]
"""

import sys
import argparse
from api import APIKeyManager

def main():
    parser = argparse.ArgumentParser(description='API Key Manager - Quản lý keys và đẩy lên GitHub')
    parser.add_argument('command', choices=['add', 'remove', 'list', 'auto', 'push', 'menu'], 
                       help='Lệnh cần thực hiện')
    parser.add_argument('--folder', '-f', help='Tên folder (cho lệnh add/remove/list)')
    parser.add_argument('--key', '-k', help='Key tùy chỉnh (cho lệnh add)')
    parser.add_argument('--count', '-c', type=int, default=1, help='Số lượng keys (cho lệnh auto)')
    
    args = parser.parse_args()
    
    manager = APIKeyManager()
    
    if args.command == 'menu':
        manager.interactive_menu()
        return
    
    if args.command == 'add':
        if not args.folder:
            print("❌ Vui lòng chỉ định folder với --folder")
            return
        
        if args.folder not in manager.get_api_folders():
            print(f"❌ Folder '{args.folder}' không tồn tại")
            return
        
        new_key = manager.add_key(args.folder, args.key)
        if new_key:
            manager.update_version(args.folder)
    
    elif args.command == 'remove':
        if not args.folder:
            print("❌ Vui lòng chỉ định folder với --folder")
            return
        
        if not args.key:
            print("❌ Vui lòng chỉ định key với --key")
            return
        
        if manager.remove_key(args.folder, args.key):
            manager.update_version(args.folder)
    
    elif args.command == 'list':
        if args.folder:
            if args.folder not in manager.get_api_folders():
                print(f"❌ Folder '{args.folder}' không tồn tại")
                return
            manager.list_keys(args.folder)
        else:
            for folder in manager.get_api_folders():
                manager.list_keys(folder)
    
    elif args.command == 'auto':
        manager.auto_generate_keys(args.count)
    
    elif args.command == 'push':
        manager.git_operations()

if __name__ == "__main__":
    main() 