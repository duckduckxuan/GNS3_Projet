<h1>IPv6 Adresse configuration</h1>
Router> enable <br>  
Router# configure terminal <br>
Router(config)# ipv6 unicast-routing<br>
Router(config)# end<br>
Router#<br><br>

Router(config)# interface name number<br>
Router(config-if)# ipv6 enable<br>
Router(config-if)# ipv6 address ipv6-address/prefix-length<br>
Router(config-if)# no shutdown<br>

interface: show ipv6 interface<br>

routing table:<br>
Router# show ipv6 route (on Cisco)<br>
route -A inet6 (on Linux)

<h1>RIP</h1>
Router(config)# ipv6 router rip process name<br>
Router(config-rtr)# redistribute connected<br>
Router(config-if)# ipv6 rip process name enable<br>

<h1>OSPF</h1>

***Choose an OSPF process-id as a positive integer and define the router-id as X.X.X.X, where X is the number associate to your router:*** <br><br>
Router# configure terminal<br>
Router(config)# ipv6 router ospf <process-id><br>
Router(config-rtr)# router-id <router-id><br><br>

***Activate the OSPF protocol on the backbone interface. Make sure you use the same OSPF processid as the one declared earlier:***<br><br>
Router(config)# interface <name> <number><br>
Router(config-if)# ipv6 ospf <process-id> area <area-id><br><br>

***You can verify the state of the adjacency between two neighbors, and the link-state database on a
router (which for now contains only local information) with the following commands:***<br><br>
Router# show ipv6 ospf neighbor<br>
Router# show ipv6 ospf database<br>
Router# show ipv6 ospf database router<br>

<h1>BGP</h1>

show bgp ipv6 unicast neighbors (to verify the state of the BGP session)<br>
clear bgp ipv6 unicast * (to reset the BGP sessions)<br>
show bgp ipv6 unicast (to see the BGP table)<br>
show ipv6 route bgp (to see the BGP routes)<br><br>

***First, one has to configure the BGP routing process on the routers. For enabling IPv6 BGP routing process use the following commands:***<br><br>
Router(config)# router bgp <as-number><br>
Router(config-router)# no bgp default ipv4-unicast<br>
Device(config-router)# bgp router-id <X.X.X.X><br><br>

***Second, to establish a BGP session between routers R2 and R3 in the figure above, the network administrator of AS112 must first configure on R2 the IP address of R3 on the R2-R3 link and the AS number of R3. Router R2 then regularly tries to establish the BGP session with R3. R3 only agrees to establish the BGP session with R2 once it has been configured with the IP address of R2 and its AS number.***<br>
***To establish a BGP session between two routers, use the following commands:***<br><br>
Router(config-router)# neighbor <ipv6-address> remote-as <as-number><br>
Router(config-router)# address-family ipv6 unicast<br>
Router(config-router-af)# neighbor <ipv6-address> activate<br><br>

***First, one needs to create an access-list:***<br><br>
Router(config)# ipv6 access-list <name-acl><br>
Router(config-ipv6-acl)# {permit|deny} <ipv6-source-prefix> <ipv6-dest-prefix><br>
***This access-list, will then be used by the route-map:***<br><br>
Router(config)# route-map <map-tag> {permit|deny} <sequence-number><br>
Router(config-route-map)# match ipv6 address <name-acl><br>
***Once the route-map created, it has to be applied to a neighbor:***<br><br>
Router(config-router-af)# neighbor <ipv6-address> route-map <map-tag> {in|out}<br>

