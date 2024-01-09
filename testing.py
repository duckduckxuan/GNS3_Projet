import gns3fy
import json
import os
import requests
import random


try:
    file_name = 'router_info_new.json'
    file = os.path.join(os.path.dirname(__file__), file_name)
    with open(file, 'r') as f:
        data = json.load(f)

except FileNotFoundError:
    print("Configuration file not found.")

# Create GNS server
server_url = "http://localhost:3080"
server = gns3fy.Gns3Connector(server_url)

# # Check connection to the GNS3 server
# try:
#     response = requests.get(f"{server_url}/v2/version")
#     response.raise_for_status()
#     print("Connection OK")
#     print(f"GNS3 version: {response.json()['version']}")
# except requests.exceptions.HTTPError as e:
#     print(f"Error, HTTP error: {e}")
# except requests.exceptions.ConnectionError:
#     print("Error, can't connect to the server")
# except requests.exceptions.Timeout:
#     print("Error, request timed out")
# except requests.exceptions.RequestException as e:
#     print(f"Connection failed, error: {e}")

# Open the project if existant, else create it
project_name  = "GNS3 Project"
all_projects= server.projects_summary(is_print=False)

if project_name in [project[0] for project in all_projects]:
    gns_project = gns3fy.Project(name=project_name, connector=server)

else:
    gns_project = server.create_project(name=project_name)

gns_project.get()


for AS_name, AS_info in data['system'].items():

    for router_name, router_info in AS_info['router'].items():
        
        node = gns3fy.Node(project_id=gns_project.project_id, name=router_name, node_type="dynamips", connector=server, template="c7200")
        node.create()
        node.start()
        

