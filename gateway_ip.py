import requests
import pickle
# 假设你已实现密码加密函数 encrypt_password
base_url = "http://tplogin.cn"
with open("../pwd.pkl", "rb") as f:
    encrypted_pwd = pickle.load(f)

def get_ipaddr():
    # 1. 加密密码
    # encrypted_pwd = encrypt_password(password)

    # 2. 构造登录数据并发送请求
    login_data = {"method": "do", "login": {"password": encrypted_pwd}}
    login_response = requests.post(base_url, json=login_data)

    # 3. 从响应中提取 stok
    stok = login_response.json()["stok"]  # 具体解析方式依实际返回JSON结构而定

    # 4. 使用 stok 获取信息，例如在线主机列表
    api_url = f"{base_url}/stok={stok}/ds"
    # host_info_data = {"hosts_info": {"table": "online_host"}, "method": "get"}
    wan_info = {"network":{"name":["wan_status"]}, "method": "get"}
    info_response = requests.post(api_url, json=wan_info)

    ipaddr = info_response.json()["network"]["wan_status"]["ipaddr"]

    return ipaddr

if __name__ == "__main__":
    ipaddr = get_ipaddr()

# 5. 处理并输出 info_response.json() 中的信息
# print(ipaddr)