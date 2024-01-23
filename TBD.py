import json
import re

# Reading the JSON file
with open('router_info_full.json', 'r') as file:
    auto_sys = json.load(file)

# Generating configuration for each router
for as_info in auto_sys['AS']:
    config = generate_router_config(as_info)
    with open(f"{as_info['routers']['name']}_config.cfg", 'w') as file:
        file.write(config)

# 移动生成文件至GNS3 project文件夹（未完成）


def generate_router_config(as_info):
    # Generate start information
    config = [
        "!\r"*3,
        "!",
        "version 15.2",
        "service timestamps debug datetime msec",
        "service timestamps log datetime msec",
        "!",
        f"hostname {as_info['routers']['name']}",
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
    # TBD


# Configure Loopback Interface
def config_loopback(as_info):
    loopback_range = as_info['loopback_range']

    config.append("interface Loopback0")
    config.append(" no ip address")
    config.append(f" ipv6 address {ip_loopback}")#json文件里自动分配地址（未完成）
    config.append(" ipv6 enable")

    if router_info['name'] in rip:
        config.append(" ipv6 rip 2001 enable")
    else:
        config.append(" ipv6 ospf 2002 area 0")

    config.append("!")


# Configure each interface (需要修改，未完成)
def config_interface():
    for interface in router_info['interfaces']:
        config.append(f"interface {interface['name']}")
        config.append(" no ip address")

        if interface['neighbor'] == "None":
            config.append(" shutdown")

        if interface['name'] == "FastEthernet0/0":
            config.append(" duplex full")
        else:
            config.append(" negotiation auto")

        config.append(f" ipv6 address {interface['ip_address']}")
        config.append(" ipv6 enable")
        config.append("!")

# Configure bgp neighbor
        

#Configure ipv6 neighbor
        
        
# Configure the first part of ending infomation
    partie_1 = [
        "!",
        "ip forward-protocol nd",
        "!\r!",
        "no ip http server",
        "no ip http secure-server",
        "!"
    ]

    for i in partie_1:
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

    # Configure the second part of ending information
    partie_2 = [
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
        "end"
    ]

    for i in partie_2:
        config.append(i)

    return "\n".join(config)
