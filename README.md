# SDNdbg
SDN Flow Analyzer - SDN/NFV debugging as a Services  (DBGaaS)

A Django based project to help simplify the analysis and debugging of complex SDN + NFVi
networks.  This is an active project with the first milestone targeted at providing detailed
interactive graphical display of Switch, ports, links, and flows within and ONOS SDN Controller
cluster. It is anticipated that this will be available in early summer of 2016.

The second milestone will be the integration of OVS switch, port, and flow information as
well as KVM/libvirt and Linux bridging / virtual Ethernet information from a Liberty-based
OpenStack installation.  The anticipated date for this milestone is late Summer to early
Fall of 2016.

A third milestone will be the integration of OpenDaylight into the project. No completion date
is available at this time.

# Installation Instructions

This project is currently under construction.  The initial release will target a stand-alone
Django collection of applications that will be managed through a browser.  Toward the middle
end of the second milestone, I hope to provide OpenStack Horizon inte

## Requirements

In progress...  I will likely target only Linux (Ubuntu 15.04+ and Fedora 23) initially but all
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

