import json
from allocate_addres import *
from configuration import *


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
connections_matrix = generate_connections_matrix(all_routers, as_mapping)
#print(connections_matrix_name)

routers_info = generate_routers_dict(all_as)
#print(routers_info)

connection_counts = {"111": 0, "112": 0, "border": 0}
for conn in connections_matrix:
    connection_counts[conn[1]] += 1

"""
with open('router_configs.txt', "w") as file:
    for as_obj in all_as:
        file.write(str(as_obj) + "\n\n")
"""
"""
with open('router_configs.txt', "w") as file:
    for as_index in all_as:
        for router in as_index.routers:
            router_loopback = generate_loopback(router.name, as_index.loopback_range)
            router_id = generate_router_id(router.name)
            generate_interface_addresses(router.name, router.interfaces, connections_matrix, connection_counts)
            router_config = generate_config(router.name, router_id, router_loopback, router.interfaces)
            file.write(router_config + "\n\n")
"""


for as_index in all_as:
    for router in as_index.routers:
        config = []  # Initialize config for each router

        router_loopback = generate_loopback(router.name, as_index.loopback_range)
        router_id = generate_router_id(router.name)
        generate_interface_addresses(router.name, router.interfaces, connections_matrix, connection_counts)

        config.extend(config_head(router.name))
        config.extend(config_loopback(router_loopback, as_index.protocol))
        config.extend(config_interface(router.interfaces, as_index.protocol))  # Pass interface, not router.interfaces
        config.extend(config_bgp(router, router_id, as_index.routers, connections_matrix_name, routers_info))
        config.extend(config_end(as_index.protocol, router_id, as_index.routers, connections_matrix_name))
        
        with open(f"{router.name}_config.cfg", 'w') as file:
            file.write('\n'.join(config))


# 移动生成文件至GNS3 project文件夹（未完成）