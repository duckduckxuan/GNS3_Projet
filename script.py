from gns3fy import Gns3Connector, Project, Node, Link
import requests


# Create GNS3 server object
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



# Create or get the project
project = Project(name="projet_gns3", connector=server)
try:
    project.get()
    print("project loaded successfully")
except Exception as e:
    print(f"failed to load project: {e}")
    exit()

# Create nodes in the project
node1 = Node(project_id=project.project_id, name="R1", node_type="dynamips", template_id="77e90525-2ffb-4b4e-91ec-3d3c86f76392", connector=server)
node1.start()