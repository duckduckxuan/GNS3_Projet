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




def generate_connections_matrix_name(routers, AS):
    connections = []
    for router in routers:
        router_as = AS[router.name]
        for interface in router.interfaces:
            if interface['neighbor'] != "None":
                router_name = router.name
                neighbor_name = interface['neighbor']

                neighbor_as = AS[neighbor_name]
                if router_as != neighbor_as:
                    state = "border"
                else:
                    state = router_as

                connection = tuple(sorted([router_name, neighbor_name]))
                connection = (connection, state)

                if connection not in connections:
                    connections.append(connection)

    connections.sort(key=lambda x: x[0]) 
    return connections


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