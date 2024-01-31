from allocate_addres import *
import ipaddress

# Configure head of file
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


# Configure Loopback Interface
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


# Configure each interface
def config_interface(interfaces, protocol, router, connections_matrix_name):
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

                if protocol == "RIP" and not ipv6_address.startswith("2001:192:170:"):
                    config.append(" ipv6 rip 2001 enable")

                elif protocol == "OSPF":  # Changed to elif for better practice
                    config.append(" ipv6 ospf 2002 area 0")

        config.append("!")

    return config  # Moved return statement outside the loop


# Configure bgp neighbor
def config_bgp(router, router_id, routers, connections_matrix_name, routers_dict):
    config = []
    current_as = routers_dict[router.name]['AS']
    neighbor_liste = []

    config.append(f"router bgp {current_as}")
    config.append(f" bgp router-id {router_id}")
    config.append(" bgp log-neighbor-changes")
    config.append(" no bgp default ipv4-unicast")

    if router.router_type == "eBGP":
        neighbor_ip = None

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
                    for routeur in routers:
                        if routeur.name == neighbor:
                            for interface in routeur.interfaces:
                                if interface['neighbor'] == router.name:
                                    neighbor_ip = interface.get('ipv6_address', '')
                                    break

                    if neighbor_ip:
                        as_number = routers_dict[neighbor]['AS']
                        config.append(f" neighbor {neighbor_ip[:-3]} remote-as {as_number}")
                        neighbor_liste.append(neighbor_ip[:-3])

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
    networks = []
    for interface in router.interfaces:
        ip_addr = interface.get('ipv6_address', '')
        if ip_addr:
            try:
                network = ipaddress.IPv6Network(ip_addr, strict=False)
                networks.append(network)
            except ValueError:
                print(f"Invalid IPv6 addresse: {ip_addr}")

    # Sort subnet
    networks.sort(key=lambda net: (net.network_address, net.prefixlen))

    # Add subnets to configuration
    for network in networks:
        config.append(f"  network {str(network)}")

    # Activate neighbor IP loopback
    for ip_neighbor in neighbor_liste:
        config.append(f"  neighbor {ip_neighbor} activate")

    config.append(" exit-address-family")
    config.append("!")

    return config

      
# Configure end of file
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

    # passive interface ospf eBGP
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
                            break
            
                    config.append(f" passive-interface {interface_name}")

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
        "end\r"
    ]

    config.extend(part)

    return config
