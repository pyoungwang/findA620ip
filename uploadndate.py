#!/usr/bin/env python3
# simple_poll_client.py

import requests
import time
import json
import hashlib
import os
from pathlib import Path

import gateway_ip

class PluginUpdater:
    def __init__(self):
        self.config = {
            'version_url': 'https://raw.githubusercontent.com/pyoungwang/findA620ip/main/version.json',
            'plugin_dir': Path('./plugin'),
            'config_file': Path('plugin_config.json')
        }
        self.current_version = self.get_current_version()
    
    def get_current_version(self):
        """获取当前版本"""
        try:
            with open(self.config['config_file'], 'r') as f:
                config = json.load(f)
                return config.get('version', '1.0.0')
        except:
            return '1.0.0'
    
    def fetch_latest_info(self):
        """获取最新版本信息"""
        try:
            response = requests.get(self.config['version_url'], timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取版本信息失败: {e}")
            return None
    
    def verify_file_integrity(self, file_path, expected_hash):
        """验证文件完整性"""
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return file_hash == expected_hash
    
    def download_update(self, download_url):
        """下载更新文件"""
        try:
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            temp_file = Path('/tmp/plugin_update.zip')
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return temp_file
        except Exception as e:
            print(f"下载更新失败: {e}")
            return None
    
    def apply_update(self, update_file, latest_info):
        """应用更新"""
        # 这里根据你的插件格式实现具体的更新逻辑
        # 例如：解压文件、替换文件、更新配置等
        
        # 备份当前版本
        backup_dir = Path(f"./backup_{self.current_version}")
        if not backup_dir.exists():
            self.config['plugin_dir'].replace(backup_dir)
        
        # 更新版本配置
        with open(self.config['config_file'], 'w') as f:
            json.dump({'version': latest_info['version']}, f, indent=2)
        
        print(f"更新完成: {self.current_version} -> {latest_info['version']}")
        self.current_version = latest_info['version']
        
        # 清理临时文件
        update_file.unlink()
    
    def check_and_update(self):
        """检查并更新"""
        print(f"检查更新... (当前版本: {self.current_version})")
        
        latest_info = self.fetch_latest_info()
        if not latest_info:
            return
        
        if latest_info['version'] != self.current_version:
            print(f"发现新版本: {latest_info['version']}")
            
            # 下载更新
            update_file = self.download_update(latest_info['download_url'])
            if update_file and self.verify_file_integrity(update_file, latest_info.get('file_hash', '')):
                self.apply_update(update_file, latest_info)
            else:
                print("文件验证失败，取消更新")
    
    def run(self):
        ip = gateway_ip.get_ipaddr()
        self.check_and_update()

if __name__ == '__main__':
    updater = PluginUpdater()
    updater.run()