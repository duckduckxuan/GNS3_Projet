import gns3fy
import requests
from requests.auth import HTTPBasicAuth

# GNS3 服务器地址和端口
server_url = "http://localhost:3080"

# 用户名和密码（如果有设置的话）



# 创建 GNS3 服务器对象
server = gns3fy.Gns3Connector(server_url)

try:
    # 发送请求并包含基本认证
    response = requests.get(f"{server_url}/v2/version")
    response.raise_for_status()
    print("连接成功")
    print(f"GNS3 服务器版本: {response.json()['version']}")
except requests.exceptions.HTTPError as e:
    print(f"连接失败，HTTP 错误: {e}")
except requests.exceptions.ConnectionError:
    print("连接失败，无法连接到服务器")
except requests.exceptions.Timeout:
    print("连接失败，请求超时")
except requests.exceptions.RequestException as e:
    print(f"连接失败，错误: {e}")
