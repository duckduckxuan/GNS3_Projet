import json

class Router:
    def __init__(self, name, router_type, interfaces, loopback_range):
        self.name = name
        self.router_type = router_type
        self.interfaces = interfaces
        self.loopback_range = loopback_range
        
class AS:
    def __init__(self, number, ip_range, loopback_range, protocol, routers):
        self.number = number
        self.ip_range = ip_range
        self.loopback_range = loopback_range
        self.protocol = protocol
        self.routers = [Router(router['name'], router['type'], router['interfaces'], loopback_range) for router in routers]

def generate_connections_matrix(routers, AS):
    connections = []
    for router in routers:
        router_as = AS[router.name]
        for interface in router.interfaces:
            if interface['neighbor'] != "None":
                router_index = int(router.name[1:])
                neighbor_index = int(interface['neighbor'][1:])

                neighbor_as = AS[interface['neighbor']]
                if router_as != neighbor_as:
                    state = "border"
                else:
                    state = router_as

                connection = tuple(sorted([neighbor_index, router_index]))
                connection = (connection, state)

                if connection not in connections:
                    connections.append(connection)

    connections.sort(key=lambda x: x[0]) 
    return connections

def generate_loopback(name, loopback_range):
    router_number = int(name[1:])
    return f"{loopback_range[:-4]}{router_number}::1/128"

def generate_interface_addresses(name, interfaces, connections, connection_counts):
    for interface in interfaces:
        if interface['neighbor'] != "None":
            router_index = int(name[1:])
            neighbor_index = int(interface['neighbor'][1:])
            connection = tuple(sorted([neighbor_index, router_index]))

            state = None
            for conn in connections:
                if conn[0] == connection:
                    state = conn[1]
                    break

            if state == "border":
                ip_range = "2001:192:170:0::/64"
            elif state == "111":
                ip_range = "2001:192:168:0::/64"
            elif state == "112":
                ip_range = "2001:192:169:0::/64"

            connection = (connection,state)
            connection_index = connections.index(connection)

            if connection_index < connection_counts["111"]:
                subnet = connection_index
            elif connection_counts["111"] <= connection_index < connection_counts["111"] + connection_counts["border"]:
                subnet = connection_index- connection_counts["111"]
            else:
                subnet = connection_index- connection_counts["111"] - connection_counts["border"]
            

            address_number = 1 if router_index < neighbor_index else 2
            ipv6_address = f"{ip_range[:-6]}{subnet+1}::{address_number}/64"
            interface['ipv6_address'] = ipv6_address

def generate_router_id(name):
    router_number = ''.join(filter(str.isdigit, name))
    return '.'.join([router_number] * 4)

def generate_routers_dict(all_as):
    routers_dict = {}
    for as_obj in all_as:
        for router in as_obj.routers:
            loopback_address = generate_loopback(router.name, as_obj.loopback_range)
            router_dict = {
                'loopback': loopback_address,
                'AS': as_obj.number
            }
            routers_dict[router.name] = router_dict
    return routers_dict

"""
def generate_router_config(router, connections_matrix, connection_counts):
    loopback = generate_loopback(router.name, router.loopback_range)
    router_id = generate_router_id(router.name)
    generate_interface_addresses(router.name, router.interfaces, connections_matrix, connection_counts)

    config = [
        "!\r"*3,
        "!",
        "version 15.2",
        "service timestamps debug datetime msec",
        "service timestamps log datetime msec",
        "!",
        f"hostname {router_info['name']}",
        "!",
        "boot-start-marker",
        "boot-end-marker",
        "!\r"*2 + "!",
        "no aaa new-model",
        "no ip icmp rate-limit unreachable",
        "ip cef",
        "!\r"*5 + "!",
        "no ip domain lookup",
        "ipv6 unicast-routing",
        "ipv6 cef",
        "!\r!",
        "multilink bundle-name authenticated",
        "!\r"*8 + "!",
        "ip tcp synwait-time 5",
        "!\r"*11 + "!",
    ]

    # Loopback and interfaces configuration
    config.extend([
        "interface Loopback0",
        " no ip address",
        f" ipv6 address {loopback}",
        " ipv6 enable",
        "!"
    ])

    # Dynamic interfaces configuration
    for interface in router.interfaces:
        if 'ipv6_address' in interface:
            config.extend([
                f"interface {interface['name']}",
                " no ip address",
                f" ipv6 address {interface['ipv6_address']}",
                " no shutdown",
                "!"
            ])

    # Protocol-specific settings (modify as needed)
    # ...

    return "\n".join(config)
"""
    

# Read JSON file
with open('router_infos_TBD.json', 'r') as file:
    data = json.load(file)

all_as = [AS(as_info['number'], as_info['IP_range'], as_info['loopback_range'], as_info['protocol'], as_info['routers']) 
          for as_info in data['AS']]

# Generate AS mapping and connections matrix
as_mapping = {router.name: as_index.number for as_index in all_as for router in as_index.routers}
all_routers = [router for as_index in all_as for router in as_index.routers]
connections_matrix = generate_connections_matrix(all_routers, as_mapping)

# Count connection types
connection_counts = {"111": 0, "112": 0, "border": 0}
for conn in connections_matrix:
    connection_counts[conn[1]] += 1

"""
# Generate and write configurations
for as_index in all_as:
    for router in as_index.routers:
        config = generate_router_config(router, connections_matrix, connection_counts)
        with open(f"{router.name}_config.cfg", 'w') as file:
            file.write(config)
"""
