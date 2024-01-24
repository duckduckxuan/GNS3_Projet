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


# Configure bgp neighbor(eBGP部分待修改)
def config_bgp(router, router_id, routers, connections_matrix_name, routers_dict):
    config = []
    current_as = routers_dict[router.name]['AS']

    config.append(f"router bgp {current_as}")
    config.append(f" bgp router-id {router_id}")
    config.append(" bgp log-neighbor-changes")
    config.append(" no bgp default ipv4-unicast")

####################################################################################
    myself = None
    neighbor = None
    neighbor_ip = None

    # 初始化循环变量
    i = 0
    found = False

    # 使用 while 循环查找边界邻居(没问题了)
    while i < len(connections_matrix_name) and not found:
        ((r1, r2), state) = connections_matrix_name[i]

        if state == 'border':
            if router.name == r1:
                myself = r1
                neighbor = r2
                found = True
                print(f"找到{myself}的邻居{neighbor}了")
            elif router.name == r2:
                myself = r2
                neighbor = r1
                found = True
                print(f"找到{myself}的邻居{neighbor}了")

        i += 1

    # 如果找到邻居(找不到)
    if neighbor:
        for routeur in routers:
            if routeur.name == neighbor:
                for interface in routeur.interfaces:
                    if interface['neighbor'] == myself:
                        neighbor_ip = interface['ipv6_address']
                        print(f"找到邻居ip了{neighbor_ip}")
                        break


        if neighbor_ip:
            as_number = routers_dict[neighbor]['AS']
            config.append(f" neighbor {neighbor_ip} remote-as {as_number}")



#####################################################################################3

    # iBGP
    neighbor_liste = []
    for routeur_name, routeur_info in routers_dict.items():
        if routeur_name != router.name and routeur_info['AS'] == current_as:
            config.append(f" neighbor {routeur_info['loopback'][:-4]} remote-as {routeur_info['AS']}")
            config.append(f" neighbor {routeur_info['loopback'][:-4]} update-source Loopback0")
            neighbor_liste.append(routeur_info['loopback'][:-4])

    config.append(" !")
    config.append(" address-family ipv4")
    config.append(" exit-address-family")
    config.append(" !")
    config.append(" address-family ipv6")

    # Announce neighbor subnet
    for interface in router.interfaces:
        ip_addr = interface.get('ipv6_address', '')
        if ip_addr:
            network = ip_addr[:-4]+ip_addr[-3:]
            config.append(f"  network {network}")

    # Activate neighbor IP loopback
    for ip_neighbor in neighbor_liste:
        config.append(f"  neighbor {ip_neighbor} activate")

    config.append(" exit-address-family")
    config.append("!")

    return config

      
# Configure end of file(已完成，待修改)
def config_end(protocol, router_id, router, connections_matrix_name):
    config = [
        "ip forward-protocol nd",
        "!\r!",
        "no ip http server",
        "no ip http secure-server",
        "!"
    ]

    # Configure part of protocol
    if protocol == "RIP":
        config.append("ipv6 router rip 2001")
        config.append(" redistribute connected")
    if protocol == "OSPF":
        config.append("ipv6 router ospf 2002")
        config.append(f" router-id {router_id}")

####################################################################################################
    # 找eBGP接口，passive ospf(有问题，找不到接口，待修改)
    if protocol == "OSPF" and router.router_type == "eBGP":
        interface_name = None
        
        for elem in connections_matrix_name:
            ((r1, r2), state) = elem

            if state == 'border':
                if router.name == r1:
                    neighbor = r2
                elif router.name == r2:
                    neighbor = r1
                else:
                    neighbor = None

                if neighbor:
                    for interface in router.interfaces:
                        if interface['neighbor'] == neighbor:
                            interface_name = interface['name']
                            #print(f"{router.name}找到eBGP邻居对应接口: {interface_name}")
                            break
            
                    config.append(f" passive-interface {interface_name}")
##################################################################################################################

    part = [
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

    config.extend(part)

    return config
