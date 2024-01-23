class Router:
    def __init__(self, name, router_type, interfaces):
        self.name = name
        self.router_type = router_type
        self.interfaces = interfaces

    def __str__(self):
        return f"Router(Name: {self.name}, Type: {self.router_type}, Interfaces: {self.interfaces})"
        
class AS:
    def __init__(self, number, ip_range, loopback_range, protocol, routers):
        self.number = number
        self.ip_range = ip_range
        self.loopback_range = loopback_range
        self.protocol = protocol
        self.routers = [Router(router['name'], router['type'], router['interfaces']) for router in routers]

    def __str__(self):
        router_str = '\n  '.join(str(router) for router in self.routers)
        return f"AS(Number: {self.number}, IP Range: {self.ip_range}, Loopback Range: {self.loopback_range}, Protocol: {self.protocol}, Routers:\n  {router_str})"



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


def generate_config(name, router_id, loopback, interfaces):
    config = f"hostname {name}\n"
    config += f"router-id {router_id}\n" 
    config += f"interface loopback0\n ipv6 address {loopback}\n"
    for interface in interfaces:
        config += f"interface {interface['name']}\n"
        if 'ipv6_address' in interface:
            config += f" ipv6 address {interface['ipv6_address']}\n"
    
    return config


"""   
with open('router_infos_test.json', 'r') as file:
    data = json.load(file)

all_as = [AS(as_info['number'], as_info['IP_range'], as_info['loopback_range'], as_info['protocol'], as_info['routers']) 
          for as_info in data['AS']]

as_mapping = {}
for as_index in all_as:
    for router in as_index.routers:
        as_mapping[router.name] = as_index.number

all_routers = [router for as_index in all_as for router in as_index.routers]
connections_matrix = generate_connections_matrix(all_routers, as_mapping)

connection_counts = {"111": 0, "112": 0, "border": 0}
for conn in connections_matrix:
    connection_counts[conn[1]] += 1

for as_index in all_as:
    for router in as_index.routers:
        router_loopback = generate_loopback(router.name, as_index.loopback_range)
        router_id = generate_router_id(router.name)
        generate_interface_addresses(router.name, router.interfaces, connections_matrix, connection_counts)
        router_config = generate_config(router.name, router_id, router_loopback, router.interfaces)
        print(router_config)


with open('router_configs.txt', "w") as file:
    for as_index in all_as:
        for router in as_index.routers:
            router_loopback = generate_loopback(router.name, as_index.loopback_range)
            router_id = generate_router_id(router.name)
            generate_interface_addresses(router.name, router.interfaces, connections_matrix, connection_counts)
            router_config = generate_config(router.name, router_id, router_loopback, router.interfaces)
            file.write(router_config + "\n\n")
"""          
