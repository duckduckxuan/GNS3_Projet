from allocate_addres import *

"""
# Reading the JSON file
with open('router_info_full.json', 'r') as file:
    auto_sys = json.load(file)

# Generating configuration for each router
for as_info in auto_sys['AS']:
    config = generate_router_config(as_info)
    with open(f"{as_info['routers']['name']}_config.cfg", 'w') as file:
        file.write(config)

"""



# Configure head of file(已完成)
def config_head(name):
    config = [
        "!\r"*3,
        "!",
        "version 15.2",
        "service timestamps debug datetime msec",
        "service timestamps log datetime msec",
        "!",
        f"hostname {name}",
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
    return config


# Configure Loopback Interface(已完成)
def config_loopback(ip_loopback, protocol):
    config = []
    config.append("interface Loopback0")
    config.append(" no ip address")
    config.append(f" ipv6 address {ip_loopback}")
    config.append(" ipv6 enable")

    if protocol == "RIP":
        config.append(" ipv6 rip 2001 enable")
    if protocol == "OSPF":
        config.append(" ipv6 ospf 2002 area 0")

    config.append("!")
    return config


# Configure each interface(已完成)
def config_interface(ipv6_address, interfaces, protocol):
    config = []
    for interface in interfaces:
        config.append(f"interface {interface['name']}")
        config.append(" no ip address")

        if interface['neighbor'] == "None":
            config.append(" shutdown")

            if interface['name'] == "FastEthernet0/0":
                config.append(" duplex full")
            else:
                config.append(" negotiation auto")

        else:
            if interface['name'] == "FastEthernet0/0":
                config.append(" duplex full")
            else:
                config.append(" negotiation auto")

            config.append(f" ipv6 address {ipv6_address}")
            config.append(" ipv6 enable")

            if protocol == "RIP":
                config.append(" ipv6 rip 2001 enable")
            if protocol == "OSPF":
                config.append(" ipv6 ospf 2002 area 0")

        config.append("!")
        return config

# Configure bgp neighbor(需要找到邻居的ip_loopback地址)(未完成)
def config_bgp(router, router_id, routers, connections_matrix_name, routers_dict):
    config = []
    config.append(f"router bgp {router.number}")
    config.append(f" bgp router-id {router_id}")
    config.append(" bgp log-neighbor-changes")
    config.append(" no bgp default ipv4-unicast")

    for elem in connections_matrix_name:
        ((r1, r2), state) = elem
        if state == 'border':
            if router.name == r1:
                for interface in router.interfaces:
                    if interface['neighbor'] == r2:
                        neighbor = r2
                        neighbor_interface = interface['neighbor_interface']
            elif router.name == r2:
                for interface in router.interfaces:
                    if interface['neighbor'] == r1:
                        neighbor = r1
                        neighbor_interface = interface['neighbor_interface']
    for routeur in routers:
        if routeur.name == neighbor:
            for interface in routeur.interfaces:
                if interface['name'] == neighbor_interface:
                    ip_neighbor = routeur.interfaces['ipv6_address']
    as_number = routers_dict[neighbor]['AS']
    config.append(f" neighbor {ip_neighbor} remote-as {as_number}")
    for routeur in routers_dict:
        if routeur.key != router.name:
            config.append(f" neighbor {routeur.value['loopback']} remote-as {routeur.value['AS']}")
            config.append(f" neighbor {routeur.value['loopback']} update-source Loopback0")
    config.append(" !")
    config.append(" address-family ipv4")
    config.append(" exit-address-family")
    config.append(" !")
    config.append(" address-family ipv6")
    return config

   
"""        
# Configure the first part of ending infomation(未完成)
def config_end():
    config = []
    part1 = [
        "!",
        "ip forward-protocol nd",
        "!\r!",
        "no ip http server",
        "no ip http secure-server",
        "!"
    ]

    for i in part1:
        config.append(i)

    # Configure part of protocol
    if router_info['name'] in rip:
        config.append("ipv6 router rip 2001")
        config.append(" redistribute connected")
    else:
        config.append("ipv6 router ospf 2002")
        config.append(f" router-id {router_info['id']}") # json文件里加router id (待完成)

    if router_info['name']=="R8":
        config.append(" passive-interface GigabitEthernet1/0")

    if router_info['name']=="R9":
        config.append(" passive-interface FastEthernet0/0")

    part2 = [
        "!\r"*3 + "!",
        "control-plane",
        "!\r!",
        "line con 0",
        " exec-timeout 0 0",
        " privilege level 15",
        " logging synchronous",
        " stopbits 1",
        "line aux 0",
        " exec-timeout 0 0",
        " privilege level 15",
        " logging synchronous",
        " stopbits 1",
        "line vty 0 4",
        " login",
        "!\r!",
        "end\r"
    ]

    for i in part2:
        config.append(i)
"""