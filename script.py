from gns3fy import Gns3Connector, Project, Node, Link
import requests
import os
import json


# Load json file
file = os.path.join(os.path.dirname(__file__), 'router_info.json')
with open(file, 'r') as f:
    data = json.load(f)


# Create GNS3 server
server_url = "http://localhost:3080"
server = Gns3Connector(server_url)


# Check connection to the GNS3 server
try:
    response = requests.get(f"{server_url}/v2/version")
    response.raise_for_status()
    print("Connection OK")
    print(f"GNS3 version: {response.json()['version']}")
except requests.exceptions.HTTPError as e:
    print(f"Error, HTTP error: {e}")
except requests.exceptions.ConnectionError:
    print("Error, can't connect to the server")
except requests.exceptions.Timeout:
    print("Error, request timed out")
except requests.exceptions.RequestException as e:
    print(f"Connection failed, error: {e}")


"""
# Get all templates ID in the GNS3
try:
    response = requests.get(f"{server_url}/v2/templates")
    response.raise_for_status()
    templates = response.json()
    for template in templates:
        print(f"Name: {template['name']}, ID: {template['template_id']}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.ConnectionError:
    print("Connection error")
except requests.exceptions.Timeout:
    print("Timeout error")
except Exception as e:
    print(f"An error occurred: {e}")
"""


# Create or get the project
project = Project(name="projet_gns3", connector=server)
try:
    project.get()
    print("project loaded successfully")
except Exception as e:
    print(f"failed to load project: {e}")
    exit()


# Create nodes in the project
template_id = "77e90525-2ffb-4b4e-91ec-3d3c86f76392"
for as_name, as_info in data['system'].items():
    for router_name in as_info['router']:
        node = Node(project_id=project.project_id, name=router_name, node_type="dynamips", connector=server, template_id=template_id)
        node.create()
        node.start()

        print(f"Node {router_name} created and started with Node ID: {node.node_id}")