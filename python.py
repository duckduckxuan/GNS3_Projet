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
    print("connection ok")
    print(f"GNS3 version: {response.json()['version']}")
except requests.exceptions.HTTPError as e:
    print(f"error, HTTP error: {e}")
except requests.exceptions.ConnectionError:
    print("error, can't connect to the server")
except requests.exceptions.Timeout:
    print("error, request timed out")
except requests.exceptions.RequestException as e:
    print(f"connection failed, error: {e}")
