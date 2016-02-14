'''


@author:    Chip Boling
@copyright: 2015 Boling Consulting Solutions. All rights reserved.
@license:   Artistic License 2.0, http://opensource.org/licenses/Artistic-2.0
@contact:   support@bcsw.net
@deffield   updated: Updated
'''

#import nova
import neutron
import keystone
import pprint
import libvirt.discovery as virtDisc

def _neutronDiscovery(result, verbose=0):
    '''
    Discover all nodes in the network that are available through 
    OpenStack APIs specific to Neutron networking
    
    TODO: This will change radically, for now, just do some hardcoded calls
          to various interfaces and see what is available.  Evenutally this
          will be consolidated once patterns emerge.
    '''
    result['networkAgents'] = neutron.agentList()
    
    result['gatewayDevices'] = neutron.gatewayDeviceList()
    result['gateways']       = neutron.networkGatewayList()
    
    # Get the tenant list
    
    tenantList = keystone.tenantList()
    result['tenants']    = {}
    
    for tenant in tenantList:
        # all networks associated with this tenant
        
        result['tenants'][tenant.name] = {}
        result['tenants'][tenant.name]['networks'] = neutron.networkList(tenant)
        result['tenants'][tenant.name]['subnets']  = neutron.subnetList(tenant)
        
        result['tenants'][tenant.name]['ports']    = neutron.portList(tenant)
        result['tenants'][tenant.name]['routers']  = neutron.routerList(tenant)
        
        """
         
         |  
         |  list_health_monitors = with_params(*args, **kwargs)
         |
         tenant['floating-ip]      = neutron.floatingIpList(tenant)
         tenant['firewalls']         = neutron.firewallList(tenant)
         tenant['firewall-policies'] = neutron.firewallPolicyList(tenant)
         tenant['firewall-rules']    = neutron.firewallRuleList(tenant)
         |  list_ikepolicies = with_params(*args, **kwargs)
         |  
         |  list_ipsec_site_connections = with_params(*args, **kwargs)
         |  
         |  list_ipsecpolicies = with_params(*args, **kwargs)
         |  
         |  list_l3_agent_hosting_routers = with_params(*args, **kwargs)
         |  list_extensions = with_params(*args, **kwargs)
         |  
         |  list_members = with_params(*args, **kwargs)
         |  
         |  list_metering_label_rules = with_params(*args, **kwargs)
         |  
         |  list_metering_labels = with_params(*args, **kwargs)
         |  
         |  list_net_partitions = with_params(*args, **kwargs)
         |  
         |  list_network_profile_bindings(self, **params)
         |      Fetch a list of all tenants associated for a network profile.
         |  
         |  list_network_profiles = with_params(*args, **kwargs)
         |  
         |  list_networks_on_dhcp_agent = with_params(*args, **kwargs)
         |  
         |  list_packet_filters = with_params(*args, **kwargs)
         |  
         |  list_policy_profile_bindings = with_params(*args, **kwargs)
         |  
         |  list_policy_profiles = with_params(*args, **kwargs)
         |  
         |  list_pools = with_params(*args, **kwargs)
         |  
         |  list_pools_on_lbaas_agent = with_params(*args, **kwargs)
         |  
         |  
         |  list_qos_queues = with_params(*args, **kwargs)
         |  
         |  list_quotas = with_params(*args, **kwargs)
         |   
         |  list_routers_on_l3_agent = with_params(*args, **kwargs)
         |  
         |  list_security_group_rules = with_params(*args, **kwargs)
         |  
         |  list_security_groups = with_params(*args, **kwargs)
         |  
         |  list_service_providers = with_params(*args, **kwargs)
         |  
         |  
         |  list_vips = with_params(*args, **kwargs)
         |  
         |  list_vpnservices = with_params(*args, **kwargs)
        """


def _libVirtDiscover(result, verbose=0):
    '''
    Discover all nodes in the network that are available through 
    the libVirt Python api.  While a separate library from use in OpenStack,
    we mainly only care about VM instances spawned by OpenStack
    
    TODO: This will change radically, for now, just do some hardcoded calls
          to various interfaces and see what is available.  Evenutally this
          will be consolidated once patterns emerge.
    '''
    virtDisc.discover(result, verbose)

def discover(verbose=0):
    '''
    Discover all nodes in the network that are available through 
    OpenStack APIs
    
    TODO: This will change radically, for now, just do some hardcoded calls
          to various interfaces and see what is available.  Evenutally this
          will be consolidated once patterns emerge.
    '''
        
    # TODO: Call into any needed APIs

    print 'TODO: Openstack: Discover'

    result = {}
    result['libvirt'] = {}
    result['neutron'] = {}
    result['libvirt'] = {}

    # Discover information an any running instances

    _libVirtDiscover(result['libvirt'], verbose=verbose)

    # Discover any exising network config from the Neutron network service

    _neutronDiscovery(result['neutron'], verbose=verbose)

    # Discover any running virtual instances
    
    virtDisc.discover(result['libvirt'], verbose=verbose)
    
    # Pretty print for debug now

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)

    #nova.discoverAll()
    
    return result