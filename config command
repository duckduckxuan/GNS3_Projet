RIP:
Router> enable
Router# configure terminal
Router(config)# ipv6 unicast-routing
Router(config)# end
Router#

Router(config)# interface name number
Router(config-if)# ipv6 enable
Router(config-if)# ipv6 address ipv6-address/prefix-length
Router(config-if)# no shutdown

interface: show ipv6 interface

routing table:
Router# show ipv6 route (on Cisco)
route -A inet6 (on Linux)


OSPF:
Choose an OSPF process-id as a positive integer and define the router-id as X.X.X.X, where X is the number associate to your router:
Router# configure terminal
Router(config)# ipv6 router ospf <process-id>
Router(config-rtr)# router-id <router-id>

Activate the OSPF protocol on the backbone interface. Make sure you use the same OSPF processid as the one declared earlier:
Router(config)# interface <name> <number>
Router(config-if)# ipv6 ospf <process-id> area <area-id>

You can verify the state of the adjacency between two neighbors, and the link-state database on a
router (which for now contains only local information) with the following commands:
Router# show ipv6 ospf neighbor
Router# show ipv6 ospf database
Router# show ipv6 ospf database router

BGP:

show bgp ipv6 unicast neighbors (to verify the state of the BGP session)
clear bgp ipv6 unicast * (to reset the BGP sessions)
show bgp ipv6 unicast (to see the BGP table)
show ipv6 route bgp (to see the BGP routes)

First, one has to configure the BGP routing process on the routers. For enabling IPv6 BGP routing process use the following commands:
Router(config)# router bgp <as-number>
Router(config-router)# no bgp default ipv4-unicast
Device(config-router)# bgp router-id <X.X.X.X>

Second, to establish a BGP session between routers R2 and R3 in the figure above, the network administrator of AS112 must first configure on R2 the IP address of R3 on the R2-R3 link and the AS number
of R3. Router R2 then regularly tries to establish the BGP session with R3. R3 only agrees to establish the BGP session with R2 once it has been configured with the IP address of R2 and its AS number.
To establish a BGP session between two routers, use the following commands:
Router(config-router)# neighbor <ipv6-address> remote-as <as-number>
Router(config-router)# address-family ipv6 unicast
Router(config-router-af)# neighbor <ipv6-address> activate

First, one needs to create an access-list:
Router(config)# ipv6 access-list <name-acl>
Router(config-ipv6-acl)# {permit|deny} <ipv6-source-prefix> <ipv6-dest-prefix>
This access-list, will then be used by the route-map:
Router(config)# route-map <map-tag> {permit|deny} <sequence-number>
Router(config-route-map)# match ipv6 address <name-acl>
Once the route-map created, it has to be applied to a neighbor:
Router(config-router-af)# neighbor <ipv6-address> route-map <map-tag> {in|out}

