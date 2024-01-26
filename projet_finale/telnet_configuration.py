from allocate_addres import *
import ipaddress

# Configure Loopback Interface(已完成)
def config_loopback(ip_loopback, protocol):
    config = []

    config.append("enable")
    config.append("conf t")
    config.append("ipv6 unicast-routing")
    config.append("interface Loopback0")
    config.append("no ip address")
    config.append(f"ipv6 address {ip_loopback}")
    config.append("ipv6 enable")

    if protocol == "RIP":
        config.append(" ipv6 rip 2001 enable")
    if protocol == "OSPF":
        config.append(" ipv6 ospf 2002 area 0")

    config.append("end")

    return config


# Configure each interface(已完成)
def config_interface(interfaces, protocol, router, connections_matrix_name):
    config = []

    for interface in interfaces:
        config.append("conf t")

        config.append(f"interface {interface['name']}")
        config.append("no ip address")

        if interface['neighbor'] == "None":
            config.append("shutdown")

        else:
            ipv6_address = interface.get('ipv6_address', '')  # Get the IPv6 address from the interface dict

            if ipv6_address:
                config.append(f"ipv6 address {ipv6_address}")
                config.append("ipv6 enable")
                config.append("no shutdown")

                if protocol == "RIP" and not ipv6_address.startswith("2001:192:170:"):
                    config.append("end")
                    config.append('conf t')
                    config.append("ipv6 router rip 2001")
                    config.append("redistribute connected")
                    config.append("end")

                    config.append("conf t")
                    config.append(f"interface {interface['name']}")
                    config.append("ipv6 rip 2001 enable")

                elif protocol == "OSPF":  # Changed to elif for better practice
                    config.append("end")
                    config.append('conf t')
                    config.append("ipv6 router ospf 2002")
                    config.append(f"router-id {router.name[1:]}.{router.name[1:]}.{router.name[1:]}.{router.name[1:]}")
                    
                    config.append("end")

                    config.append("conf t")
                    config.append(f"interface {interface['name']}")
                    config.append("ipv6 ospf 2002 area 0")

        config.append("end")



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
                            #print(f"{router.name}找到eBGP邻居对应接口: {interface_name}")
                            break
                    
                    config.append("conf t")
                    config.append("ipv6 router ospf 2002")
                    config.append(f"passive-interface {interface_name}")
                    config.append("end")




    return config  # Moved return statement outside the loop


# Configure bgp neighbor
def config_bgp(router, router_id, routers, connections_matrix_name, routers_dict):
    config = []
    current_as = routers_dict[router.name]['AS']
    neighbor_liste = []

    config.append("conf t")
    config.append(f"router bgp {current_as}")
    config.append(f"bgp router-id {router_id}")
    config.append("no bgp default ipv4-unicast")

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
                                    print(router.name)
                                    neighbor_ip = interface.get('ipv6_address', '')
                                    print(f"找到邻居ip了{neighbor_ip}")
                                    break

                    if neighbor_ip:
                        as_number = routers_dict[neighbor]['AS']
                        config.append(f"neighbor {neighbor_ip[:-3]} remote-as {as_number}")
                        neighbor_liste.append(neighbor_ip[:-3])

    for routeur_name, routeur_info in routers_dict.items():
        if routeur_name != router.name and routeur_info['AS'] == current_as:
            config.append(f"neighbor {routeur_info['loopback'][:-4]} remote-as {routeur_info['AS']}")
            config.append(f"neighbor {routeur_info['loopback'][:-4]} update-source Loopback0")
            neighbor_liste.append(routeur_info['loopback'][:-4])


    config.append("address-family ipv6 unicast")

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
        config.append(f"network {str(network)}")

    # Activate neighbor IP loopback
    for ip_neighbor in neighbor_liste:
        config.append(f"neighbor {ip_neighbor} activate")

    config.append("end")

    return config

      
