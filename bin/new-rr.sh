#!/usr/bin/env bash

# Establish new routing & and ruling
#
# The definitive guide to all of this is the collection of the Linux Advanced Routing & Traffic
# Control resources, located at
#       				 https://lartc.org
# We use the ip command a lot...

# ALL OF THE BELOW SHOULD BE MIGRATED INTO SYSTEMD-NETWORKD, NETWORKMANAGER, OR SIMILAR!

# We rely on user-defined tables in /etc/iproute2/rt_tables, which (by default) looks like

# Linux kernel routing tables
#
#
# reserved values
#
#255     local
#254     main
#253     default
#0       unspec
#
#
# local
#
#1      inr.ruhep

# We start from scratch and populate the file with our tables.  Don't worry, the iproute2 package
# installs the file primarily in the folder /usr/share/iproute2
rm --force /etc/iproute2/rt_tables
mkdir --parent /etc/iproute2
cat << EOM > /etc/iproute2/rt_tables
2       switch.maintenance
1       new.routing
EOM

# The primary NIC
primary_nic=enp0s29f7u3c2 # make this enp5s0 one day!!!
primary_nic_addr=10.1.0.10
primary_nic_net=10.1.0.0/24
primary_nic_gw=10.1.0.1
iots_gw=172.17.0.1
soho_gw=172.18.0.1

# Address
ip address flush ${primary_nic}
ip address add ${primary_nic_addr}/24 dev ${primary_nic}

# Route & gateway
ip route flush table new.routing
ip route del ${primary_nic_net} dev ${primary_nic} src ${primary_nic_addr} table main # Trivial route!
ip route add ${primary_nic_net} dev ${primary_nic} src ${primary_nic_addr} table new.routing
ip route add default via ${primary_nic_gw} dev ${primary_nic} table new.routing

# When to use
ip rule flush table new.routing
ip rule add from ${primary_nic_addr}/32 table new.routing
ip rule add to ${primary_nic_addr}/32 table new.routing
ip rule add to ${primary_nic_gw}/32 table new.routing
ip rule add to ${iots_gw}/32 table new.routing
ip rule add to ${soho_gw}/32 table new.routing

# The NIC that serves as the access to the switch's maintenance interface
# We have a mini-net: just the switch, the peer, and the broadcast address
sw_maint_nic=enp0s29f7u4c2
sw_maint_nic_addr=10.0.0.253
sw_maint_nic_net=10.0.0.252/30
sw_maint_nic_gw=10.0.0.254

# Address
ip address flush ${sw_maint_nic}
ip address add ${sw_maint_nic_addr}/30 dev ${sw_maint_nic}

# Route & gateway
ip route flush table switch.maintenance
ip route del ${sw_maint_nic_net} dev ${sw_maint_nic} src ${sw_maint_nic_addr} table main # Trivial route!
ip route add ${sw_maint_nic_net} dev ${sw_maint_nic} src ${sw_maint_nic_addr} table switch.maintenance
ip route add default via ${sw_maint_nic_gw} dev ${sw_maint_nic} table switch.maintenance

# When to use
ip rule flush table switch.maintenance
ip rule add from ${sw_maint_nic_addr}/32 table switch.maintenance
ip rule add to ${sw_maint_nic_addr}/32 table switch.maintenance
ip rule add to ${sw_maint_nic_gw}/32 table switch.maintenance

# Show the results of the above
ip route list table main
echo
ip route list table new.routing
echo
ip route list table switch.maintenance
echo
ip rule show
