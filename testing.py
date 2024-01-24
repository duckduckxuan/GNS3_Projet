import gns3fy
import json
import time
import telnetlib

nodes_ports = {}


def get_nodes(project_name):

    server = gns3fy.Gns3Connector("http://localhost:3080")

    projet = gns3fy.Project(name=project_name, connector=server)
    
    projet.get()
    projet.open()

    for node in projet.nodes:
        node.get()
        nodes_ports[node.name] = node.console


def config_loopback(router,protocol):
    router_number = router["name"][1]

    basic_config = f"""interface Loopback0\r
                    no ip address\r
                    ipv6 address 2001:DB8:{router_number}::1/128\r
                    ipv6 enable\r"""
    
    if protocol == "RIP":
        basic_config += "ipv6 rip 2001 enable\r"
    elif protocol == "OSPF":
        basic_config += "ipv6 ospf 2002 area 0\r"

    return basic_config


def config_interfaces(interface,protocol):
    if interface["neighbor"] == "None":
        no_neighbor = f"""interface {interface["name"]}\r
                        no ip address\r
                        shutdown\r
                        negotiation auto\r"""
        
        return no_neighbor

    else:
        #TODO WHICH ADDRESS TO PUT
        basic_config = f"""interface {interface["name"]}\r
                            no ip address\r
                            duplex full\r
                            ipv6 address 2001:192:168:5::2/64\r
                            ipv6 enable\r"""
        
        if protocol == "RIP":
            basic_config += "ipv6 rip 2001 enable\r"
        elif protocol == "OSPF":
            basic_config += "ipv6 ospf 2002 area 0\r"

        return basic_config
        

def config_bgp(router,as_number):
    router_number = router["name"][1]

    basic_config = f"""router bgp {as_number}\r
                        bgp router-id {router_number}.{router_number}.{router_number}.{router_number}\r
                        bgp log-neighbor-changes\r
                        no bgp default ipv4-unicast\r"""
    

    if router["type"] == "eBGP":
        if as_number == 111:
            basic_config += """neighbor 2001:192:170:1::2 remote-as 112\r"""

        else:
            basic_config += """neighbor 2001:192:170:1::2 remote-as 111\r"""

    if as_number == 111:

        for i in range(1,8):
            if i == int(router_number):
                continue
            
            basic_config += f"""neighbor 2001:DB8:{i}::1 remote-as {as_number}\r
                                neighbor 2001:DB8:{i}::1 update-source Loopback0\r"""
            
    elif as_number == 112:
        for i in range(8,15):
            if i == int(router_number):
                continue

            basic_config += f"""neighbor 2001:DB8:{i}::1 remote-as {as_number}\r
                                neighbor 2001:DB8:{i}::1 update-source Loopback0\r"""
            
    
    basic_config += """address-family ipv4\r
                    exit-address-family\r
                    address-family ipv6\r"""
    

    if as_number == 111:
        for i in range(1,8):
            if i == int(router_number):
                continue

            basic_config += f"""neighbor 2001:DB8:{i}::1 activate\r"""
            
    elif as_number == 112:
        for i in range(8,15):
            if i == int(router_number):
                continue

            basic_config += f"""neighbor 2001:DB8:{i}::1 activate\r"""


    basic_config += """exit-address-family\r"""
    

    return basic_config


def telnet_write(config,port):
    
    try:
        print(port)
        tn = telnetlib.Telnet('localhost',port)
        time.sleep(1)
        tn.write(config)
        time.sleep(1)
        tn.write(b"end\r")

    except Exception as e:
        print(f"Error: {e}")


get_nodes("TEMPLATE GNS3")
print(nodes_ports)

with open('router_infos_test.json', 'r') as file:
    data = json.load(file)


for AutoSys in data["AS"]:
    
    as_number = int(AutoSys["number"])
    protocol = AutoSys["protocol"]

    for router in AutoSys["routers"]:
        config = ""
        config += config_loopback(router,protocol)

        for interface in router["interfaces"]:
            config += config_interfaces(interface,protocol)

        config += config_bgp(router,as_number)

        telnet_write(config.encode(), nodes_ports[router["name"]])




