import gns3fy
import telnetlib
import time
import json
from allocate_addres import *
from telnet_configuration import *


with open('projet_finale/router_infos_TBD.json', 'r') as file:
    data = json.load(file)

all_as = [AS(as_info['number'], as_info['IP_range'], as_info['loopback_range'], as_info['protocol'], as_info['routers']) 
          for as_info in data['AS']]

as_mapping = {}
for as_index in all_as:
    for router in as_index.routers:
        as_mapping[router.name] = as_index.number

all_routers = [router for as_index in all_as for router in as_index.routers]

for router in all_routers:
    print(f"router-id {router.name[1:]}.{router.name[1:]}.{router.name[1:]}.{router.name[1:]}")