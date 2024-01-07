import gns3fy
import requests

# GNS3 server address
server_url = "http://localhost:3080"

# Create GNS3 server object
server = gns3fy.Gns3Connector(server_url)

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
project = gns3fy.Project(name="projet_gns3", connector=server)
try:
    project.get()  # Attempt to get the project, if it doesn't exist, it will throw an exception
except Exception:
    project.create()  # If the project doesn't exist, create it

# Ensure the project has a project_id
if not project.project_id:
    print("Failed to get or create a project with a valid project_id.")

# Create a new node in the project
try:
    node = gns3fy.Node(project_id=project.project_id, name="R1", node_type="dynamips", template_id="77e90525-2ffb-4b4e-91ec-3d3c86f76392", connector=server)
    node.create()
    print(f"Created node {node.name} with ID {node.node_id}")
except Exception as e:
    print(f"Failed to create node: {e}")