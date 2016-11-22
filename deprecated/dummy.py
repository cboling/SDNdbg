#
# For scratchpad work...
#
services_have = ['delete',
                 'description', 'enabled', 'get',
                 'human_id', 'id', 'is_loaded', 'links', 'manager',
                 'name', 'set_loaded', 'to_dict', 'type']
services = [
    {u'description': u'Heat CloudFormation Service',
     u'enabled'    : True,
     u'id'         : u'009f75deb1884bd2968ef1b45df8fec6',
     u'links'      : {u'self': u'http://192.168.1.121:35357/v3/services/009f75deb1884bd2968ef1b45df8fec6'},
     u'name'       : u'heat-cfn',
     u'type'       : u'cloudformation'},
    {u'description': u'Neutron Service',
     u'enabled'    : True,
     u'id'         : u'148d79e0a4c64e33bb99fe176a6439e6',
     u'links'      : {u'self': u'http://192.168.1.121:35357/v3/services/148d79e0a4c64e33bb99fe176a6439e6'},
     u'name'       : u'neutron',
     u'type'       : u'network'},
    {u'description': u'Nova Compute Service (Legacy 2.0)',
     u'enabled'    : True,
     u'id'         : u'16a8f56bb4a84596970b04ff57e0fb89',
     u'links'      : {u'self': u'http://192.168.1.121:35357/v3/services/16a8f56bb4a84596970b04ff57e0fb89'},
     u'name'       : u'nova_legacy',
     u'type'       : u'compute_legacy'},
    {u'description': u'Cinder Volume Service',
     u'enabled'    : True,
     u'id'         : u'2e1857969f2047ebaebf96ade6f750bf',
     u'links'      : {u'self': u'http://192.168.1.121:35357/v3/services/2e1857969f2047ebaebf96ade6f750bf'},
     u'name'       : u'cinder',
     u'type'       : u'volume'},
    {u'description': u'Heat Orchestration Service',
     u'enabled'    : True,
     u'id'         : u'53ab3c92219c439f96354e7c89d213e8',
     u'links'      : {u'self': u'http://192.168.1.121:35357/v3/services/53ab3c92219c439f96354e7c89d213e8'},
     u'name'       : u'heat',
     u'type'       : u'orchestration'},
    {u'description': u'Cinder Volume Service V2',
     u'enabled'    : True,
     u'id'         : u'8c52643aa0024040852d244357094043',
     u'links'      : {u'self': u'http://192.168.1.121:35357/v3/services/8c52643aa0024040852d244357094043'},
     u'name'       : u'cinderv2',
     u'type'       : u'volumev2'},
    {u'description': u'Nova Compute Service',
     u'enabled'    : True,
     u'id'         : u'92cc6613c2bb46c0b0591ee9a957d405',
     u'links'      : {u'self': u'http://192.168.1.121:35357/v3/services/92cc6613c2bb46c0b0591ee9a957d405'},
     u'name'       : u'nova',
     u'type'       : u'compute'},
    {u'description': u'Tacker NFV Orchestration Service',
     u'enabled'    : True,
     u'id'         : u'aeba0eecb7704ac0a9d64147e7c0dea7',
     u'links'      : {u'self': u'http://192.168.1.121:35357/v3/services/aeba0eecb7704ac0a9d64147e7c0dea7'},
     u'name'       : u'tacker',
     u'type'       : u'nfv-orchestration'},
    {u'description': u'Glance Image Service',
     u'enabled'    : True,
     u'id'         : u'ce74c4cb091341f985af7dfb5923364e',
     u'links'      : {u'self': u'http://192.168.1.121:35357/v3/services/ce74c4cb091341f985af7dfb5923364e'},
     u'name'       : u'glance',
     u'type'       : u'image'},
    {u'enabled': True,
     u'id'     : u'daeaa33b679a47389a71229e897f79eb',
     u'links'  : {u'self': u'http://192.168.1.121:35357/v3/services/daeaa33b679a47389a71229e897f79eb'},
     u'name'   : u'keystone',
     u'type'   : u'identity'}

]
Endpoints_have = ['delete', 'enabled', 'get',
                  'human_id', 'id', 'interface', 'is_loaded', 'links',
                  'manager', 'region', 'region_id', 'service_id',
                  'set_loaded', 'to_dict', 'url']

endpoints = [
    {u'enabled'   : True,
     u'id'        : u'1804c8a2655340118c333bdbd13032cb',
     u'interface' : u'public',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/1804c8a2655340118c333bdbd13032cb'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'53ab3c92219c439f96354e7c89d213e8',
     u'url'       : u'http://192.168.1.121:8004/v1/$(tenant_id)s'},
    {u'enabled'   : True,
     u'id'        : u'1b367565381d4c1ab57bac5d39cfec86',
     u'interface' : u'internal',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/1b367565381d4c1ab57bac5d39cfec86'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'009f75deb1884bd2968ef1b45df8fec6',
     u'url'       : u'http://192.168.1.121:8000/v1'},
    {u'enabled'   : True,
     u'id'        : u'282374e8047d43029692e4914fe92bf8',
     u'interface' : u'public',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/282374e8047d43029692e4914fe92bf8'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'16a8f56bb4a84596970b04ff57e0fb89',
     u'url'       : u'http://192.168.1.121:8774/v2/$(tenant_id)s'},
    {u'enabled'   : True,
     u'id'        : u'2b3a5580f60a43dba1be503c55e67e28',
     u'interface' : u'internal',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/2b3a5580f60a43dba1be503c55e67e28'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'53ab3c92219c439f96354e7c89d213e8',
     u'url'       : u'http://192.168.1.121:8004/v1/$(tenant_id)s'},
    {u'enabled'   : True,
     u'id'        : u'3606646d23f74e3593e52bf50ddd0b7d',
     u'interface' : u'admin',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/3606646d23f74e3593e52bf50ddd0b7d'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'8c52643aa0024040852d244357094043',
     u'url': u'http://192.168.1.121:8776/v2/$(tenant_id)s'},
     {u'enabled'   : True,
      u'id'        : u'360c6ddb3a584705aff792a6571dd884',
      u'interface' : u'admin',
      u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/360c6ddb3a584705aff792a6571dd884'},
      u'region'    : u'RegionOne',
      u'region_id' : u'RegionOne',
      u'service_id': u'ce74c4cb091341f985af7dfb5923364e',
      u'url'       : u'http://192.168.1.121:9292'},
    {u'enabled'   : True,
     u'id'        : u'3f168b5dc3494603859aa306c0463c94',
     u'interface' : u'internal',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/3f168b5dc3494603859aa306c0463c94'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'148d79e0a4c64e33bb99fe176a6439e6',
     u'url'       : u'http://192.168.1.121:9696/'},
    {u'enabled'   : True,
     u'id'        : u'4ac2665ea786420ebbc4e1d99ecca2fe',
     u'interface' : u'internal',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/4ac2665ea786420ebbc4e1d99ecca2fe'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'16a8f56bb4a84596970b04ff57e0fb89',
     u'url'       : u'http://192.168.1.121:8774/v2/$(tenant_id)s'},
    {u'enabled'   : True,
     u'id'        : u'5464c30d44cb46f4ba0cb9ad47179e21',
     u'interface' : u'admin',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/5464c30d44cb46f4ba0cb9ad47179e21'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'148d79e0a4c64e33bb99fe176a6439e6',
     u'url'       : u'http://192.168.1.121:9696/'},
    {u'enabled'   : True,
     u'id'        : u'57d2f489b22b4f0d9a15b58e1d992fe7',
     u'interface' : u'internal',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/57d2f489b22b4f0d9a15b58e1d992fe7'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'ce74c4cb091341f985af7dfb5923364e',
     u'url'       : u'http://192.168.1.121:9292'},
    {u'enabled'   : True,
     u'id'        : u'61f7ad3ad24349aa8d4dff7fa515e52d',
     u'interface' : u'public',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/61f7ad3ad24349aa8d4dff7fa515e52d'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'148d79e0a4c64e33bb99fe176a6439e6',
     u'url'       : u'http://192.168.1.121:9696/'},
    {u'enabled'   : True,
     u'id'        : u'634c3388830646118c785ae98c224ba5',
     u'interface' : u'public',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/634c3388830646118c785ae98c224ba5'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'009f75deb1884bd2968ef1b45df8fec6',
     u'url'       : u'http://192.168.1.121:8000/v1'},
    {u'enabled'   : True,
     u'id'        : u'642c29eedb0948f286cd6b560846aff0',
     u'interface' : u'admin',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/642c29eedb0948f286cd6b560846aff0'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'53ab3c92219c439f96354e7c89d213e8',
     u'url'       : u'http://192.168.1.121:8004/v1/$(tenant_id)s'},
    {u'enabled'   : True,
     u'id'        : u'6d29e2bfb0b740e1a01ef23df21c338c',
     u'interface' : u'internal',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/6d29e2bfb0b740e1a01ef23df21c338c'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'daeaa33b679a47389a71229e897f79eb',
     u'url'       : u'http://192.168.1.121:5000/v2.0'},
    {u'enabled'   : True,
     u'id'        : u'70202138693a480f89dd185038695dde',
     u'interface' : u'internal',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/70202138693a480f89dd185038695dde'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'92cc6613c2bb46c0b0591ee9a957d405',
     u'url'       : u'http://192.168.1.121:8774/v2.1/$(tenant_id)s'},
    {u'enabled'   : True,
     u'id'        : u'7e6c1d6cd8a84dbcb913073d0160ab41',
     u'interface' : u'internal',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/7e6c1d6cd8a84dbcb913073d0160ab41'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'8c52643aa0024040852d244357094043',
     u'url'       : u'http://192.168.1.121:8776/v2/$(tenant_id)s'},
    {u'enabled'   : True,
     u'id'        : u'83ca0127011a4f07be31766a3e3e2341',
     u'interface' : u'admin',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/83ca0127011a4f07be31766a3e3e2341'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'92cc6613c2bb46c0b0591ee9a957d405',
     u'url'       : u'http://192.168.1.121:8774/v2.1/$(tenant_id)s'},
    {u'enabled'   : True,
     u'id'        : u'96d67c619a864aef853cf1a56d1d1077',
     u'interface' : u'internal',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/96d67c619a864aef853cf1a56d1d1077'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'aeba0eecb7704ac0a9d64147e7c0dea7',
     u'url'       : u'http://192.168.1.121:9890/'},
    {u'enabled'   : True,
     u'id'        : u'a584570a7a6c4e6b87fe7cd3d196f4d1',
     u'interface' : u'admin',
     u'links'     : {u'self': u'http://192.168.1.121:35357/v3/endpoints/a584570a7a6c4e6b87fe7cd3d196f4d1'},
     u'region'    : u'RegionOne',
     u'region_id' : u'RegionOne',
     u'service_id': u'009f75deb1884bd2968ef1b45df8fec6',
     u'url'       : u'http://192.168.1.121:8000/v1'}
]

# Output of Openstack endpoint list when running as distinct docker containters
# The 'interface' will be 'admin', 'internal', or 'public' and perhaps public may
# be the best to use (for IP address). Really is the IP we are going after but may
# need to resolve the URL !!!!  But this address may not be visible from where we are running
# this APP from.  Good thing to add to README !!!
D
2016 - 11 - 22
16:28:27, 228
INFO:SDNdbg:sync_object: entry.OpenCORD
2016 - 11 - 22
16:28:27, 681
INFO:SDNdbg:OpenStack
Controller: DBG
Endpoints:
[ < Endpoint
enabled = True, id = 043
eb0e22e094d1193e595f7e3179d38, interface = public, links = {
                                                            u'self': u'https://keystone.cord.lab:5000/v3/endpoints/043eb0e22e094d1193e595f7e3179d38'}, region = RegionOne, region_id = RegionOne, service_id = 10
b253c6d6d94eb4a7406c3cdb597c3e, url = https: // keystone.cord.lab:5000 / v2
.0 >,
< Endpoint
enabled = True, id = 89
c879bac0c1428080d5bc977e896ea3, interface = public, links = {
                                                             u'self': u'https://keystone.cord.lab:5000/v3/endpoints/89c879bac0c1428080d5bc977e896ea3'}, region = RegionOne, region_id = RegionOne, service_id = b10d50746b334de3a15914e42476cfff, url = https: // neutron - api.cord.lab:9696 >,
< Endpoint
enabled = True, id = fa2a8656e1754bc9bdfc1041b464ace8, interface = public, links = {
                                                                                    u'self': u'https://keystone.cord.lab:5000/v3/endpoints/fa2a8656e1754bc9bdfc1041b464ace8'}, region = RegionOne, region_id = RegionOne, service_id = 29
b3ee5f2a994f2ba62fcfb5e752dd04, url = https: // nova - cloud - controller.cord.lab:8774 / v2 /$(tenant_id)
s >]
2016 - 11 - 22
16:28:27, 681
ERROR:SDNdbg:Unhandled
Exception
while attempting to sync 'OpenCORD [fce38719-b102-11e6-ba8f-b8ca3ab44c0c]': TODO: Implement
this
openstack
endpoint
list - -long
+----------------------------------+-----------+--------------+--------------+---------------------------------------+---------------------------------------+----------------------------------------+
| ID | Region | Service
Name | Service
Type | PublicURL | AdminURL | InternalURL |
+----------------------------------+-----------+--------------+--------------+---------------------------------------+---------------------------------------+----------------------------------------+
| 0
db97c2830204907905c53afa645874c | RegionOne | neutron | network | https: // neutron - api.cord.lab:9696 | https: // neutron - api.cord.lab:9696 | https: // neutron - api.cord.lab:9696 |
| 1
d718fd59ee741f182e4082cdf66061f | RegionOne | keystone | identity | https: // keystone.cord.lab:5000 / v2
.0 | https: // keystone.cord.lab:35357 / v2
.0 | https: // keystone.cord.lab:5000 / v2
.0 |
| 68318969
fc6a450eade97d88064f9aea | RegionOne | ceilometer | metering | https: // ceilometer.cord.lab:8777 | https: // ceilometer.cord.lab:8777 | https: // ceilometer.cord.lab:8777 |
| ee95303d7b4f40b785713abc174d0d85 | RegionOne | glance | image | https: // glance.cord.lab:9292 | https: // glance.cord.lab:9292 | https: // glance.cord.lab:9292 |
| 5
b1040a81c1e4fd681be8c54a5114f30 | RegionOne | nova | compute | https: // nova - cloud - controller.cord.la | https: // nova - cloud - controller.cord.la | https: // nova - cloud - controller.cord.lab |
| | | | | b:8774 / v2 /$(tenant_id)
s | b:8774 / v2 /$(tenant_id)
s |:8774 / v2 /$(tenant_id)
s |
+----------------------------------+-----------+--------------+--------------+---------------------------------------+---------------------------------------+----------------------------------------+
