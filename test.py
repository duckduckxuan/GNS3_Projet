import json
import gns3fy
from gns3fy import Gns3Connector, Project, Node

# Lire le fichier JSON
with open("router_configuration.json", "r") as file:
    config_data = json.load(file)

# Se connecter au serveur GNS3
server_url = 'http://localhost:3080'
gns3_server = Gns3Connector(server_url)

# Créer ou récupérer le projet
project_name = 'Network_Configuration_Project'
try:
    project = Project(name=project_name, connector=gns3_server)
    project.create()
except gns3fy.Gns3fyException:
    project = gns3_server.get_project(name=project_name)

# RIP Configuration
rip_routers = config_data["system"]["AS111"]["router"]

for router_name, router_info in rip_routers.items():
    router = Node(project_id=project.project_id, connector=gns3_server, name=router_name, node_type="dynamips")
    router.create()

    basic_commands = [
        "enable",
        "configure terminal",
        "ipv6 unicast-routing",
        "ipv6 router rip RIP_Net",
        "exit"
    ]
    for command in basic_commands:
        router.console(command)

    # Configurer les interfaces
    for interface_info in router_info["interfaces"]:
        interface = interface_info["interface"]
        ipv6_address = interface_info["ipv6"]
        interface_commands = [
            f"interface {interface}",
            "ipv6 enable",
            f"ipv6 address {ipv6_address}",
            "ipv6 rip RIP_Net enable",
            "no shutdown",
            "exit"
        ]
        for command in interface_commands:
            router.console(command)
          
# OSPF Configuration
ospf_routers = config_data["system"]["AS112"]["router"]

for router_name, router_info in ospf_routers.items():
    router = Node(project_id=project.project_id, connector=gns3_server, name=router_name, node_type="dynamips")
    router.create()

    # OSPF 基本配置
    router_id = router_info["router_id"]
    ospf_commands = [
        "enable",
        "configure terminal",
        "ipv6 unicast-routing",
        f"ipv6 router ospf 1",
        f"router-id {router_id}",
        "exit"
    ]
    for command in ospf_commands:
        router.console(command)

    # 配置每个接口
    for interface_info in router_info["interfaces"]:
        interface = interface_info["interface"]
        ipv6_address = interface_info["ipv6"]
        ospf_interface_commands = [
            f"interface {interface}",
            "ipv6 enable",
            f"ipv6 address {ipv6_address}",
            "ipv6 ospf 1 area 0",
            "no shutdown",
            "exit"
        ]
        for command in ospf_interface_commands:
            router.console(command)


# Configurer les routeurs BGP (iBGP et eBGP)
for as_system, as_info in config_data["system"].items():
    for router_name, router_info in as_info["router"].items():
        router = Node(project_id=project.project_id, connector=gns3_server, name=router_name, node_type="dynamips")
        router.create()

        # Configuration de base BGP
        router_id = router_info["router_id"]
        as_number = as_info["id"]
        bgp_commands = [
            "enable",
            "configure terminal",
            f"router bgp {as_number}",
            "no bgp default ipv4-unicast",
            f"bgp router-id {router_id}",
            "address-family ipv6 unicast"
        ]

        # Configurer les voisins BGP (iBGP ou eBGP)
        for neighbor in router_info.get("bgp_neighbors", []):
            neighbor_ip = neighbor["ip"]
            neighbor_as = neighbor["as"]
            bgp_commands += [
                f"neighbor {neighbor_ip} remote-as {neighbor_as}",
                "neighbor {neighbor_ip} activate"
            ]

        # Appliquer la configuration BGP
        for command in bgp_commands:
            router.console(command)

        # Configuration des interfaces (si nécessaire)
        # ... (Configurer les interfaces comme dans les parties RIP et OSPF) ...

