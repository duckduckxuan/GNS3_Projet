import json
import os
import shutil
from allocate_addres import *
from configuration import *


def move_and_overwrite(source_file, target_directory):
    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # 构建目标文件路径
    target_file = os.path.join(target_directory, os.path.basename(source_file))

    # 移动文件，如果目标文件存在则覆盖
    shutil.move(source_file, target_file)



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
routers_info = generate_routers_dict(all_as)

connection_counts = {"111": 0, "112": 0, "border": 0}
for conn in connections_matrix:
    connection_counts[conn[1]] += 1


source_file = []

target_directory = [
    'gns3_final/project-files/dynamips/5a0fd657-52da-4d82-a3af-7e02a2aa3d7b',
    'gns3_final/project-files/dynamips/2ddf61d6-f681-417a-b5dd-509ac4c99dab',
    'gns3_final/project-files/dynamips/48ebb1cc-8a28-4929-813c-6ad77f2f69ff',
    'gns3_final/project-files/dynamips/9d9d8a6c-60c8-4dce-990b-a335281c1f7b',
    'gns3_final/project-files/dynamips/86d5d625-5d21-4018-af70-0aaf9ea40bbe',
    'gns3_final/project-files/dynamips/bcc0cbae-307e-4ffd-97bd-59d7c4fa37ed',
    'gns3_final/project-files/dynamips/4d565293-426d-4cb1-8041-b67726c5c161',
    'gns3_final/project-files/dynamips/31888c72-49d0-4378-8294-27fa1ae77f9f',
    'gns3_final/project-files/dynamips/74eb78d8-3e73-4879-ae7c-577fcd4f66f4',
    'gns3_final/project-files/dynamips/45331f6d-d3f2-427b-a5e6-97300343897d',
    'gns3_final/project-files/dynamips/5c562ef8-0ba4-41b9-a5ed-329d900cc3e3',
    'gns3_final/project-files/dynamips/343be9c4-fcc7-4c16-a3a3-03a8d477e09b',
    'gns3_final/project-files/dynamips/32b9c447-4652-4f82-be5a-96feafdba4e6',
    'gns3_final/project-files/dynamips/0611ba5c-e75a-4aab-9652-83885f48b5fb'
]


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
        config.extend(config_end(as_index.protocol, router_id, router, connections_matrix_name))
        
        with open(f"i{router.name[1:]}_startup-config-new.cfg", 'w') as file:
            file.write('\n'.join(config))
            source_file.append(f"i{router.name[1:]}_startup-config-new.cfg")


"""
# Move intent files to GNS3's directory
i,j = 0

while i < len(source_file) and j < len(target_directory):
    move_and_overwrite(source_file[i], target_directory[j])
    i += 1
    j += 1
"""
