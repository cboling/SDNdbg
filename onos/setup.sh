#!/bin/bash
#
# Copyright (c) 2015 - Present.  Boling Consulting Solutions, BCSW.net
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
######################################################################################
#
# Simple setup script to start LXC containers with test ONOS cluster.  See the
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


