# neutron-diag

[neutron-diag](https://github.com/larsks/neutron-diag)
developed by [Lars Kellogg-Stedman](https://github.com/larsks) in late 2013 is set of three
_bash_ scripts ran as root (or _sudo_) on a compute node to
gather information.  The one of most interest is _mk-network-dot_ which generates a
[graphviz](http://www.graphviz.org) output that can be rendered by _dot_ to show
a static representation of the networking components.  Below is an example output showing
two _cirros_ images launched by tacker that are connected to three networks each (_net0_,
_net1_, and _net_mgmt_).

![graphviz rendering](file://./pics/neutron-diag-sample.png] "Existing ONOS-SFC Networks")

For reference, the _graphviz_ input is available [here](./data/neutron-diag-sample.dot)

In the graph above, the following block types/colors are:

* instance/VM -> tomato box
* OVS bridge -> light blue oval
* Linux bridge -> olive drab oval
* veth -> light grey oval
* OVS patch port -> gold CDS (Box with a pointy end on the right)
* OVS tunnel port -> thistle CDS
* Remote -> black solid box
* Namespaces other than 'global'  -> A box with black border and devices/ports/... that it contains are located inside

The OVS tunnel and Remote block types are not shown but will appear if a 'gre' of 'vxlan' port type is discovered and the
peer is located.

See [Node Shapes](http://www.graphviz.org/doc/info/shapes.html) for more information on availabe
graphViz node shapes.

## mk-network-dot

_mk-network-dot_ creates three files (_edges_, _nodes_, and _peers_) that contain information for creating
the _graphviz_ input.  Each is described below.

> Note that all of the _LINUX_ commands below must be ran on the a specific OpenStack node and for a
> full picture of the network, you need to execute the commands on each machine and stitch them
> together manually.

## Under the hood of mk-network-dot

The following sections outline what command the _mk-network-dot_ script uses to do its magic.

### VM Instances
The _mk-network-dot_ script executes the **virsh list --name** command to get a
list of the running instances on the nova compute.  The script iterates over these instance names and
executes the following **virsh dumpxml _<instance>** command and pipes the output into **xmllint** as
shown below:

```bash
virsh dumpxml $instance | xmllint --xpath '//interface/target/@dev' -
```
This output is then used to create the 'dev' name for edges output. Sample output of the above command
for **instance-00000001** on my test system is shown below.

```xml
    <domain type='qemu' id='2'>
  <name>instance-00000001</name>
  <uuid>8c1aedc3-d016-44a0-bfc5-43fef5d5fff3</uuid>
  <metadata>
    <nova:instance xmlns:nova="http://openstack.org/xmlns/libvirt/nova/1.0">
      <nova:package version="12.0.2"/>
      <nova:name>ta-ef18-d0c5-46ee-a2c1-c21e11f6808b-vdu1-yq7nv2ijm7dz</nova:name>
      <nova:creationTime>2016-01-24 03:05:59</nova:creationTime>
      <nova:flavor name="m1.tiny">
        <nova:memory>512</nova:memory>
        <nova:disk>1</nova:disk>
        <nova:swap>0</nova:swap>
        <nova:ephemeral>0</nova:ephemeral>
        <nova:vcpus>1</nova:vcpus>
      </nova:flavor>
      <nova:owner>
        <nova:user uuid="2707537300f94b8b8c6ded48691b77af">tacker</nova:user>
        <nova:project uuid="760fc7d3a2da41528fd136ab30a8b85f">service</nova:project>
      </nova:owner>
      <nova:root type="image" uuid="f6c83ebe-81ab-47e0-9002-bd9351b1cb9f"/>
    </nova:instance>
  </metadata>
  <memory unit='KiB'>524288</memory>
  <currentMemory unit='KiB'>524288</currentMemory>
  <vcpu placement='static'>1</vcpu>
  <cputune>
    <shares>1024</shares>
  </cputune>
  <resource>
    <partition>/machine</partition>
  </resource>
  <sysinfo type='smbios'>
    <system>
      <entry name='manufacturer'>OpenStack Foundation</entry>
      <entry name='product'>OpenStack Nova</entry>
      <entry name='version'>12.0.2</entry>
      <entry name='serial'>6762aa93-dd4c-453d-bb73-2b3f0b8f54c9</entry>
      <entry name='uuid'>8c1aedc3-d016-44a0-bfc5-43fef5d5fff3</entry>
      <entry name='family'>Virtual Machine</entry>
    </system>
  </sysinfo>
  <os>
    <type arch='x86_64' machine='pc-i440fx-trusty'>hvm</type>
    <kernel>/opt/stack/data/nova/instances/8c1aedc3-d016-44a0-bfc5-43fef5d5fff3/kernel</kernel>
    <initrd>/opt/stack/data/nova/instances/8c1aedc3-d016-44a0-bfc5-43fef5d5fff3/ramdisk</initrd>
    <cmdline>root=/dev/vda console=tty0 console=ttyS0 no_timer_check</cmdline>
    <boot dev='hd'/>
    <smbios mode='sysinfo'/>
  </os>
  <features>
    <acpi/>
    <apic/>
  </features>
  <cpu>
    <topology sockets='1' cores='1' threads='1'/>
  </cpu>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' cache='none'/>
      <source file='/opt/stack/data/nova/instances/8c1aedc3-d016-44a0-bfc5-43fef5d5fff3/disk'/>
      <target dev='vda' bus='virtio'/>
      <alias name='virtio-disk0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
    </disk>
    <disk type='file' device='cdrom'>
      <driver name='qemu' type='raw' cache='none'/>
      <source file='/opt/stack/data/nova/instances/8c1aedc3-d016-44a0-bfc5-43fef5d5fff3/disk.config'/>
      <target dev='hdd' bus='ide'/>
      <readonly/>
      <alias name='ide0-1-1'/>
      <address type='drive' controller='0' bus='1' target='0' unit='1'/>
    </disk>
    <controller type='usb' index='0'>
      <alias name='usb0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x2'/>
    </controller>
    <controller type='pci' index='0' model='pci-root'>
      <alias name='pci.0'/>
    </controller>
    <controller type='ide' index='0'>
      <alias name='ide0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
    </controller>
    <interface type='bridge'>
      <mac address='fa:16:3e:7e:bb:a3'/>
      <source bridge='qbrb6b21e98-ab'/>
      <target dev='tapb6b21e98-ab'/>
      <model type='virtio'/>
      <driver name='qemu'/>
      <alias name='net0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
    </interface>
    <interface type='bridge'>
      <mac address='fa:16:3e:d7:10:2b'/>
      <source bridge='qbr5f3fe3d7-73'/>
      <target dev='tap5f3fe3d7-73'/>
      <model type='virtio'/>
      <driver name='qemu'/>
      <alias name='net1'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
    </interface>
    <interface type='bridge'>
      <mac address='fa:16:3e:a6:c3:02'/>
      <source bridge='qbrabc73b14-34'/>
      <target dev='tapabc73b14-34'/>
      <model type='virtio'/>
      <driver name='qemu'/>
      <alias name='net2'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
    </interface>
    <serial type='file'>
      <source path='/opt/stack/data/nova/instances/8c1aedc3-d016-44a0-bfc5-43fef5d5fff3/console.log'/>
      <target port='0'/>
      <alias name='serial0'/>
    </serial>
    <serial type='pty'>
      <source path='/dev/pts/52'/>
      <target port='1'/>
      <alias name='serial1'/>
    </serial>
    <console type='file'>
      <source path='/opt/stack/data/nova/instances/8c1aedc3-d016-44a0-bfc5-43fef5d5fff3/console.log'/>
      <target type='serial' port='0'/>
      <alias name='serial0'/>
    </console>
    <input type='mouse' bus='ps2'/>
    <input type='keyboard' bus='ps2'/>
    <graphics type='vnc' port='5900' autoport='yes' listen='192.168.1.121' keymap='en-us'>
      <listen type='address' address='192.168.1.121'/>
    </graphics>
    <video>
      <model type='cirrus' vram='9216' heads='1'/>
      <alias name='video0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
    </video>
    <memballoon model='virtio'>
      <alias name='balloon0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
      <stats period='10'/>
    </memballoon>
  </devices>
  <seclabel type='dynamic' model='apparmor' relabel='yes'>
    <label>libvirt-8c1aedc3-d016-44a0-bfc5-43fef5d5fff3</label>
    <imagelabel>libvirt-8c1aedc3-d016-44a0-bfc5-43fef5d5fff3</imagelabel>
  </seclabel>
</domain>
```
In the _mk-network-dot_ script, the **--xpath '//interface/target/@dev' -** is piped the above
output to create a list of devices which will be categorized as **edges**. In the above output, the
_xmllint_ output locates the following edges for the first instance:

* dev="tapb6b21e98-ab"
* dev="tap5f3fe3d7-73"
* dev="tapabc73b14-34"

Besides the devices within each VM instance, each instance itself is identified as a **node**.

### The global networking namespace

The script then calls another **sh** script called _ns-get-devs_ with an argument of **global** to
extract nodes, edges, and peers from the global namespace.

The _ns-get-devs_ script executes the **ls /sys/class/net** command and pipes the output into a
while loop and treats each output as a _device_.  Within this loop, if the _device_ equals either **lo**
or **ovs-system**, it skips that _device_.  For my test system, the full output of the **ls** command
above is:

```
    br-ext    docker0     qbr35e8a35a-d9  qbrb6b21e98-ab  qvb8b99fe12-76  qvo35e8a35a-d9  qvob6b21e98-ab  tap8b99fe12-76  virbr0
    br-int    eth0        qbr5f3fe3d7-73  qbrdd8cc769-de  qvbabc73b14-34  qvo5f3fe3d7-73  qvodd8cc769-de  tapabc73b14-34
    br-mgmt0  lo          qbr8b99fe12-76  qvb35e8a35a-d9  qvbb6b21e98-ab  qvo8b99fe12-76  tap35e8a35a-d9  tapb6b21e98-ab
    br-tun    ovs-system  qbrabc73b14-34  qvb5f3fe3d7-73  qvbdd8cc769-de  qvoabc73b14-34  tap5f3fe3d7-73  tapdd8cc769-de
```

> Unless you are supporting _nova-docker_ or _lxc/lxc_ as a virtualization subsystem, you may want to filter out
> and **docker#** and **vibr#** bridges as well.

For each **dev** _device_ above, it will execute the following command to extract out
the driver involved:

```
    driver=$(ethtool -i $dev | awk '/driver:/ {print $2}' 2> /dev/null)
```
The output for a sample number of devices above (ignoring the __awk__ filter) are:

```
    root@onos-sfc:/home/cboling/neutron-diag# ethtool -i br-ext
    driver: openvswitch
    version:
    firmware-version:
    bus-info:
    supports-statistics: no
    supports-test: no
    supports-eeprom-access: no
    supports-register-dump: no
    supports-priv-flags: no

    root@onos-sfc:/home/cboling/neutron-diag# ethtool -i tap8b99fe12-76
    driver: tun
    version: 1.6
    firmware-version:
    bus-info: tap
    supports-statistics: no
    supports-test: no
    supports-eeprom-access: no
    supports-register-dump: no
    supports-priv-flags: no

    root@onos-sfc:/home/cboling/neutron-diag# ethtool -i qvbb6b21e98-ab
    driver: veth
    version: 1.0
    firmware-version:
    bus-info:
    supports-statistics: yes
    supports-test: no
    supports-eeprom-access: no
    supports-register-dump: no
    supports-priv-flags: no

    root@onos-sfc:/home/cboling/neutron-diag# ethtool -i qbr8b99fe12-76
    driver: bridge
    version: 2.3
    firmware-version: N/A
    bus-info: N/A
    supports-statistics: no
    supports-test: no
    supports-eeprom-access: no
    supports-register-dump: no
    supports-priv-flags: no
```
The script then looks for, and processes only the _veth_, _openvswitch_, and _bridge_
driver types.  Each driver type device is saved off as in the **node** file.

#### _veth_ driver type

For the _veth_ driver type, the script extract the ifindex by running a **cat**
command on the file: _/sys/class/net/**<dev>**/ifIndex_ and the peer ifdex by
running the **ethtool -S <dev>** command and extracting the second argument of
the _peer_ifindex_ line.  The output for the **ethtool -S** command for a
sample _veth_ driver type is shown below:

```
    # ethtool -S qvo8b99fe12-76
    NIC statistics:
         peer_ifindex: 48
```

#### _bridge_ driver type

For the _bridge_ driver type, the script will pipe the output of the
**ls /sys/class/net/<dev>/brif** output and treat each output as a port and will
then save it off to the **edges* file.

An example output of the **ls** command for one of the _bridge_ driver types is
shown below:

```
    # ls /sys/class/net/qbr8b99fe12-76/brif
    qvb8b99fe12-76  tap8b99fe12-76

```

#### _openvswitch_ driver type

For the _openvswitch_ driver type, the script first checks to see if the device
is an OVS Bridge by calling the **ovs-vsctl br-exists <dev>** command. If it does it
will mark the driver type as an _ovsbridge_ and call the **ovs-vsctl list-ports <dev>** command
to get the edges.  If it is not an OVS bridge, it marks the driver type as an _ovsport_

For the sample devices above, the _br-ext_ bridge is an OVS bridge and an **ovs-vsctl list-ports
br-ext** command yields the following:

```
    ovs-vsctl list-ports br-ext
    phy-br-ext
```

### Other networking namespaces

Once the _global_ namespace has been discovered, the remaining network namespaces are
iterated (listed via **ip netns** command) and the _ns-get-devs_ script that was
used to work the _global_ namespace is executed within each namespace via the **ip
netns exec** command.

### OVS Port information

Once the namespaces have been discovered, the _mk-network-dot_ command will begin to
work on the OVS bridges and build out the _nodes_, _edges_, and _seen_ files.  The
_seen_ file is used to track ports already listed (saved as an edge) so they do not
appear twice.

The list of bridge devices to iterate over is available from the *ovs-vsctl list-br**
command.  This output is then feed into another command, **ovs-vsctl list-ports <dev>**.

> At this point, the _list-ports_ command may output some OVS ports already listed in
> the _nodes_ file.  These ports are skipped since they have already been discovered.

The port type is extracted using the **ovs-vsctl get Interface <port> type** command.

If the port type is 'patch', the peer is looked for using the **ovs-vsctl get
Interface <port> options:peer** command.  For the _patch-tun_ in my example, it has
a peer port of _patch-int_ which is an OVS port also of type 'patch'.

If the port type is 'gre' or 'vxlan', then type OVS port type is set to 'OVS tunnel'
and the peer interface is looked for using the **ovs-vsctl get Interface <port>
options:remote_ip** command.  For my example, no OVS tunnel ports were found.

The earlier **ovs-vsctl get Interface <port> type** command also returns two other
port types.  One is a empty string _""_ and the other is of type _internal_.  The
empty string port types appear to be _veth_ endpoints discovered earlier and the
_internal_ port types appear to be perhaps ports or veth endpoints inside of a
non-global network namespace.

### veth peer interfaces

The final step performed is to iterate through the _peers_ file and look for
peer interfaces for veths.  Since veths always come in pairs, once one veth has
been processed and its peer added to the _edges_ file, the dev is saved off to
the temporary _seen_ file so that edges do not appear twice.


### graphviz dot file output

Once all the information has been gathered, the nodes and edges
