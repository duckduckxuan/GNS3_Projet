import gns3fy
import telnetlib
import time
import json
from allocate_addres import *
from telnet_configuration import *



nodes_ports = {}

def get_nodes(project_name):

    server = gns3fy.Gns3Connector("http://localhost:3080")

    projet = gns3fy.Project(name=project_name, connector=server)
    
    projet.get()
    projet.open()

    for node in projet.nodes:
        node.get()
        nodes_ports[node.name] = node.console
        node.start()

    print("Starting nodes takes 1 minutes. Go grab a coffee.")
    time.sleep(60)

def telnet_write(config,port):
    
    try:
        print(port)
        tn = telnetlib.Telnet('localhost',port)
        time.sleep(1)
        tn.write(b"\r") #To start writing
        time.sleep(1)

        for command in config:
            tn.write(command.encode())
            tn.write(b"\r")
            time.sleep(0.01)

        time.sleep(1)

        tn.write(b"write\r\r")

    except Exception as e:
        print(f"Error: {e}")

get_nodes("gns3_final")
#print(nodes_ports)


with open('router_infos_TBD.json', 'r') as file:
    data = json.load(file)

all_as = [AS(as_info['number'], as_info['IP_range'], as_info['loopback_range'], as_info['protocol'], as_info['routers']) 
          for as_info in data['AS']]

as_mapping = {}
for as_index in all_as:
    for router in as_index.routers:
        as_mapping[router.name] = as_index.number

all_routers = [router for as_index in all_as for router in as_index.routers]
connections_matrix_name = generate_connections_matrix_name(all_routers, as_mapping)
#print(connections_matrix_name)
connections_matrix = generate_connections_matrix(all_routers, as_mapping)
routers_info = generate_routers_dict(all_as)

connection_counts = {"111": 0, "112": 0, "border": 0}
for conn in connections_matrix:
    connection_counts[conn[1]] += 1


for as_index in all_as:
    for router in as_index.routers:
        generate_interface_addresses(router.name, router.interfaces, connections_matrix, connection_counts)

for as_index in all_as:
    for router in as_index.routers:
        router_loopback = generate_loopback(router.name, as_index.loopback_range)
        router_id = generate_router_id(router.name)
        config = []


        config.extend(config_loopback(router_loopback, as_index.protocol))
        config.extend(config_interface(router.interfaces, as_index.protocol, router, connections_matrix_name))

        config.extend(config_bgp(router, router_id, all_routers, connections_matrix_name, routers_info))

        print(config)
        telnet_write(config,nodes_ports[router.name])


        
