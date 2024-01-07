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

# Create a new project in GNS3
try:
    project = gns3fy.Project(name="projet_gns3", connector=server)
    project.create()
    print(f"Project '{project.name}' created with ID {project.project_id}")
except Exception as e:
    print(f"Failed to create project: {e}")

# Create a new node in the project
try:
    node = gns3fy.Node(project=project, name="router1", node_type="dynamips")
    node.create()
    print(f"Created node {node.name} with ID {node.node_id}")
except Exception as e:
    print(f"Failed to create node: {e}")
