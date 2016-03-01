#!/bin/bash
#
# Simple setup script to start LXC containters with test ONOS cluster.  See the
# https://wiki.onosproject.org/display/ONOS/Multiple+instances+using+LXC file
# for more information
#
for i in onos1 onos2 onos3
do
  sudo lxc-start -n $i -d
done

echo "Cluster started, pausing 5 seconds to allow them to spin up a bit"
sleep 5

cell lxc-cluster

echo "Setting up IP Tables to allow local GUI access to $OC1 on port 8181"
sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 8181 -j DNAT --to $OC1:8181


