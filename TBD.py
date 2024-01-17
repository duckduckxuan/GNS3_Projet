import json

def generate_router_config(router_info):
    """Generate router configuration based on the provided information."""
    config = [
        "!",
        "version 15.2",
        "service timestamps debug datetime msec",
        "service timestamps log datetime msec",
        "！",
        f"hostname {router_info['name']}",
        "!",
        "boot-start-marker",
        "boot-end-marker",
        "!\r"*3,
        "no aaa new-model",
        "no ip icmp rate-limit unreachable",
        "ip cef",
        "!\r"*6,
        "no ip domain lookup",
        “ipv6 unicast-routing”，
        “ipv6 cef”，
        “!\r”*2，
        "multilink bundle-name authenticated",
        "!\r"*9,
        "ip tcp synwait-time 5",
        "!\r"*12,
    ]

    # Configure Loopback Interface
    config.append("interface Loopback0")
    config.append(f" ip address {router_info['loopback']}")
    config.append("!")

    # Configure each interface
    for interface in router_info['interfaces']:
        config.append(f"interface {interface['name']}")
        config.append(f" ip address {interface['ip_address']}")
        config.append(" no shutdown")
        config.append("!")

    

    return "\n".join(config)

# Reading the JSON file
with open('router_info_full.json', 'r') as file:
    routers = json.load(file)

# Generating configuration for each router
for router in routers['AS'][0]['routers']:
    config = generate_router_config(router)
    with open(f"{router['name']}_config.cfg", 'w') as file:
        file.write(config)
