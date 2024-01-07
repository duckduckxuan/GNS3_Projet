import gns3fy
import requests
from requests.auth import HTTPBasicAuth

# GNS3 server address & host
server_url = "http://localhost:3080"

# create GNS3 server
server = gns3fy.Gns3Connector(server_url)

try:
    # send request and check
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
