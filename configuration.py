from allocate_addres import *

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
def config_interface(interfaces, protocol):
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

            ipv6_address = interface.get('ipv6_address', '')  # Get the IPv6 address from the interface dict
            if ipv6_address:
                config.append(f" ipv6 address {ipv6_address}")
                config.append(" ipv6 enable")

                if protocol == "RIP":
                    config.append(" ipv6 rip 2001 enable")
                elif protocol == "OSPF":  # Changed to elif for better practice
                    config.append(" ipv6 ospf 2002 area 0")
                else: # 如果eBGP就什么都不加
                    pass

        config.append("!")

    return config  # Moved return statement outside the loop


# Configure bgp neighbor(需要找到邻居的ip_loopback地址)(未完成)
def config_bgp(router, router_id, routers, connections_matrix_name, routers_dict):
    config = []
    current_as = routers_dict[router.name]['AS']

    config.append(f"router bgp {current_as}")
    config.append(f" bgp router-id {router_id}")
    config.append(" bgp log-neighbor-changes")
    config.append(" no bgp default ipv4-unicast")

    myself = None
    neighbor = None
    neighbor_ip = None

    # eBGP(需要修改，现在显示不出来eBGP邻居端口ip地址)
    for elem in connections_matrix_name:
        ((r1, r2), state) = elem

        if state == 'border':
            if router.name == r1:
                myself = r1
                neighbor = r2
                print(f"找到边界邻居: {neighbor}")
            elif router.name == r2:
                myself = r2
                neighbor = r1
                print(f"找到边界邻居: {neighbor}")

        for routeur in routers:
            if routeur.name == neighbor:
                for interface in routeur.interfaces:
                    if interface['neighbor'] == myself:
                        neighbor_ip = interface['ipv6_address']
                        break
                break

        if neighbor_ip:
            as_number = routers_dict[neighbor]['AS']
            config.append(f" neighbor {neighbor_ip} remote-as {as_number}")

    # iBGP
    for routeur_name, routeur_info in routers_dict.items():
        if routeur_name != router.name and routeur_info['AS'] == current_as:
            config.append(f" neighbor {routeur_info['loopback']} remote-as {routeur_info['AS']}")
            config.append(f" neighbor {routeur_info['loopback']} update-source Loopback0")

    config.append(" !")
    config.append(" address-family ipv4")
    config.append(" exit-address-family")
    config.append(" !")
    config.append(" address-family ipv6")
    # 添加子网掩码
    # 激活所有邻居
    config.append(" exit-address-family")
    config.append("!")

    return config

      
# Configure end of file(未完成)
def config_end(protocol, router_id, routers):
    config = []
    part1 = [
        "ip forward-protocol nd",
        "!\r!",
        "no ip http server",
        "no ip http secure-server",
        "!"
    ]

    for i in part1:
        config.append(i)

    # Configure part of protocol
    if protocol == "RIP":
        config.append("ipv6 router rip 2001")
        config.append(" redistribute connected")
    if protocol == "OSPF":
        config.append("ipv6 router ospf 2002")
        config.append(f" router-id {router_id}")

    if protocol == "OSPF":
        for router in routers:
            if router.router_type == "eBGP":
                # 找到eBGP端口名称
                
        config.append(f" passive-interface {interface}")

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
        "end"
    ]

    for i in part2:
        config.append(i)

    return config