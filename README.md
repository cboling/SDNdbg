# SDNdbg
SDN Flow Analyzer - SDN/NFV debugging as a Services  (DBGaaS)

This project attempts to discover the nodes and links within an SDN/NFV network for the purposes
of debugging connectivity issues. 

Currently OpenStack as the VIM/NFVi and ONOS as the SDN controller will be supported. Future work
will include OpenDaylight SDN Controller support and perhaps more VIMs.

Initially only the KVM/QEMU compute hypervisors will be supported (primarily via libvirt) but it is
highly desireable to support container technologies.

# Installation Instructions

This project is currently under construction. It is suggested that you create a virtual Python
environment and work within that environment. The steps to create this environment are:

## Create Virtual Environment
```
    $ pip install virtualenv
    $ cd SDNdbg                 # This base directory
    $ virtualenv vENV
    $ source vENV/bin/activate
```
## Install Dependencies

```
    $ cd SDNdbg                 # This base directory
    $ source vENV/bin/activate
    $ sudo apt-get install libvirt-dev
    $ pip install -r requirements.txt
```

## Running the Application

```
    $ cd SDNdbg                 # This base directory
    $ source vENV/bin/activate
    $ ...TODO...
```


## Platform Requirements

In progress...  I will likely target only Linux (Ubuntu 16.04+ and Centos 7+) initially but all
code is expected to be in Python, HTML, JS, and CSS.  So Windows is a possibility, just not an
initial target.

# TODO List

Here is a brief outline of the planned work for the SDNdbg project. Completed tasks will either
be remove are modified with ~~strike through~~ formatting. If you are interested in helping out
on this project, please let me know by posting to the issues link at
 [https://github.com/cboling/SDNdbg/issues](https://github.com/cboling/SDNdbg/issues).

* Login Screen to provide customizable access control to debugger sessions, deployments, and
 site information.  Actual ACL enforcement will not be implemented until the middle to end of
 the second milestone effort.

* Home screen to allow user to create a deployment profile (ONOS and OpenStack sites) that provide
automated discovery of controllers and resources.  The OpenStack NFVi support will be minimal but
I feel that some discovery of OpenStack topology early in the project will help with pushing
any common needs into a set of core modules.

* ONOS Cluster discovery covering controllers, switches, ports, links, flows, and intents.  Some
information on running applications will be collected for completeness but the main effort here
is to collect the node/edge information for ONOS and present it as an interactive network graph.

* Begin UI work on ONOS Network Graph including tooltip (hover help), property dialogs (left-click),
and context sensitive menu (right-click) support.

* Implement path discovery logic for ONOS.

* Implement UI filtering capability based on path, node-depth, and other useful attributes.

* Implement diagnostic capabilities, including live traffic capture as well as traffic injection
and capture for path debugging.  This step will likely require a custom ONOS application.

* Release of Milestone 1.

