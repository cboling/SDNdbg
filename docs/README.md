# Introduction

This directory contains some information on two Open Source projects that gather
similar information.  The first application is [neutron-diag](https://github.com/larsks/neutron-diag)
developed by [Lars Kellogg-Stedman](https://github.com/larsks) in late 2013.  The second
project is
[Debugging of OVS Networking for Openstack Neutron - 'don'](https://github.com/CiscoSystems/don) developed by
[Amit Saha](https://github.com/amsaha) and [Debo~ Duta](https://github.com/ddutta) from Cisco and
demonstrated at the May 2015 OpenStack Summit in Vancouver.

Please visit each github repository for more information on each project. The breakdown
that follows is basically for my own education. The target version of OpenStack for both
investigations is the stable Liberty release.

One item to note is that the neutron-diag scripts seem to have a few issues with either Ubuntu 15.10 (the Linux
version I am running) or with OpenStack liberty.

## neutron-diag

A separate README markdown file is provided with details of the _neutron-diag_ scripts.  Based
on examination of the script outputs, there are three significant items that it places items under.
These three items are _nodes_, _edges_, and _peers_. It also identifies and tracks any network namespaces
in use.

### nodes

The nodes file is a collection of _devices_.  Each entry in the nodes file consists
of 3 items: device name, device type, and network namespace.

The device name is the name that the device goes by.  This should be shown on any output and when combined
with the machine name and network namespace, it should be unique.

The network namespace is self explanatory.  When displaying, we may wish to hide the global network namespace
name.

The device type is of most interest.  The following types were discovered during my initial look at
the neutron-diag scripts.  Note that the order the devices are discovered is important as
the scripts keep track of nodes it has already seen and does not parse them twice.

| Device Major Type | Minor Type | Notes                                                   |
|:-----------------:|:----------:| ------------------------------------------------------- |
|     instance      |            | This is a VM image gathered with the **virsh list** command.  This command does not cover any container instances (_lxc/lxd_ or _docker_).  It may also list VMs that are not launched by OpenStack                  |
|     bridge        |    linux   | Gathered with the 'ethtool -i <dev>' command where the dev is the device name (eth0, lxcbr0, ...). To read ports it walks the /sys/class/net/<dev>/brif directory (may be empty) and emits the dev & port out to the edges file.  The driver type is 'bridge'                |
|                   |    OVS     | Gathered similar to the linux bridge above.  The driver type is 'openvswitch' and 'ovs-vsctl br-exists <dev> is called to verify it actual exists. To gather the ports, it uses the 'ovs-vsctl list-ports <dev>' command and emits the dev & port out to the edges file.             |
|     port          |  hardware  | Gathered same as linux bridge but the driver type is easy to decipher.  Just output on to the 'nodes' with its driver name.  A gig port can show up with a driver type of 'e1000'.  **TODO**  need a way to gather this.. |
|                   |    veth    | Gathered same as linux bridge but driver type is 'veth' Script then gets peer index by running the 'ethtool -S <dev> and parsing the 'peer_ifindex' line. It saves the result off to the peer file.                            |
|                   |  ovspatch  | Script lists the OVS bridges with the 'ovs-vsctl list-br' command and then for each bridge device <brdev> it runs the 'ovs-vsctl list-ports <brdev>' command.  For each <port> it gets the type with the 'ovs-vsctl get Interface <port> type command. For an 'patch' port, it will get the peer with the ovs-vsctl get Interface  <port> options:peer' command. It saves the 'port' out to the nodes file and the port + peer out to the edges file.                                                   |
|                   |  ovstun    | Gathered the same as the 'tun' above but the port typeis either 'gre' or 'vxlan'. For tunnels, it gets the  remote ip 'peer' with the 'ovs-vsctl get Interface <port> options:remote_ip' command.                      |
|                   |   remote   | Gathered during 'ovstun' port identification.  **TODO** Need a way to stitch remote ports on different nodes together.                                         |


> **NOTE**: When processing device types from any APIs we write or consume, we should throw an exception
>           for unhandled types since our demo system may be more complex than what I have first looked at.

### edges

The edges file consists of entries with two columns.  Both columns are device names (nodes) that were
discovered and a link/line should be drawn between them.

### peers

The peers file seems to consists of a list of veths found on the system with related ifIndexes.  It is
used within an awk script to determine the edges between the veths.

> **NOTE** The use of the peers file and how it is used to generate edges for the veths needs more
>          attention.  It is difficult to understand with just a cursory look and perhaps there are
>          better ways to do this.

### APIs needed

The following APIs/capabilities are needed to duplicate the work of _neutron-diag_in a python environment:

#### Instances

**python-novaclient** and **python-openstackclient** are probably the prefeered way to list any VMs
that are running.  If possible, favor *python-openstackclient** over **python-novaclient**.

**libvirt** provides Python and Java bindings and may be one way to gather additional information.

From the Instances, we need at a minimum the:
* name of the Instance
* a list of interface devices (targets).  The devices may also have an alias name that would be useful to display. The
alias is the VM internal name for the network port such as 'net0' or 'eth1' where the higher level
device name is often something like 'tap5f3fe3d7-73'.
* the mac address of each interface device
* the device type of the interface

> TODO: list each an leave space for possible libraries or ways to implement what is needed.



