import gns3fy
import requests

# 创建 GNS3 服务器对象
server = gns3fy.Gns3Connector("http://localhost:3080")

try:
    response = requests.get('http://127.0.0.1:3080/v2/version')
    response.raise_for_status()  # 如果响应状态不是 200，将引发 HTTPError 异常
    print("连接成功")
    # 打印 GNS3 服务器版本
    print(f"GNS3 服务器版本: {response.json()['version']}")
except requests.exceptions.HTTPError as e:
    print(f"连接失败，HTTP 错误: {e}")
except requests.exceptions.ConnectionError:
    print("连接失败，无法连接到服务器")
except requests.exceptions.Timeout:
    print("连接失败，请求超时")
except requests.exceptions.RequestException as e:
    print(f"连接失败，错误: {e}")
