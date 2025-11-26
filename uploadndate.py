#!/usr/bin/env python3
import os
import json
import subprocess
from datetime import datetime
import pickle

import gateway_ip

def run_main_script():
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ip_address = gateway_ip.get_ipaddr()
        results = {
            "last_updated": current_time,
            "ip": ip_address
        }
        
        # 保存结果为JSON文件
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # 生成Markdown报告
        generate_markdown_report(results)
        
        print("✅ 脚本执行完成，结果文件已生成")
        return True
        
    except Exception as e:
        print(f"❌ 脚本执行失败: {e}")
        return False

def generate_markdown_report(data):
    """Markdown"""
    markdown_content = f"""# A620 ip

最后更新: **{data['last_updated']}**

## {data['ip']}

"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)

def git_operations():
    try:
        with open("../config.pkl", "rb") as f:
            config = pickle.load(f)
            email = config["user.email"]
            name = config["user.name"]
        subprocess.run(['git', 'config', 'user.email', email], check=True)
        subprocess.run(['git', 'config', 'user.name', name], check=True)
        
        # 添加所有更改
        subprocess.run(['git', 'add', 'README.md'], check=True)
        
        # 提交更改
        commit_message = f"Automated update: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # 推送到GitHub
        subprocess.run(['git', 'push'], check=True)
        
        print("✅ Git操作完成，更改已推送到GitHub")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始执行自动更新流程...")
    
    # 运行主脚本生成结果
    if run_main_script():
        # 执行Git操作
        git_operations()
    else:
        print("❌ 流程执行失败")

if __name__ == "__main__":
    main()