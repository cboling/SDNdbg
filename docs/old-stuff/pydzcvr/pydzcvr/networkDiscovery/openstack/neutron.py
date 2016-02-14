'''
Python API interface into Neutron Networking client

@author:    Chip Boling
@copyright: 2015 Boling Consulting Solutions. All rights reserved.
@license:   Artistic License 2.0, http://opensource.org/licenses/Artistic-2.0
@contact:   support@bcsw.net
@deffield   updated: Updated

@see: http://docs.openstack.org/developer/python-neutronclient/
'''

import sys
import neutronclient.v2_0.client as netClient

def _getNeutronClient(authUrl, username, password, project='admin', verbose=0):
    """
    Get the neutron client for a particular installation and project
    
    :Parameters:
        TODO (string)    Document parameters 
        
    :Returns:
        client
    :ReturnType:
        neutronclient
    """

    credentials = { 'username'    : username,
                    'password'    : password,
                    'auth_url'    : authUrl,
                    'tenant_name' : project, 
                  }

    try:
        return netClient.Client(**credentials)

    except netClient.exceptions, e:
        sys.stderr.write("neutron._getNeutronClient: " + repr(e) + "\n")

    except Exception, e:
        sys.stderr.write("neutron._getNeutronClient (other exception): " + repr(e) + "\n")

    return None, "n/a"
            
   
def agentList(verbose=0):    
    """
    TODO: Document
    
    :Parameters:
        TODO (string)    Document parameters 
        
    :Returns:
        List of network dictionaries
    :ReturnType:
        list
    """
    url      = 'http://bcsw-os-controller:35357/v2.0'     # TODO make into class/dict and pass in list of projects
    username = 'admin'
    password = 'password'

    client = _getNeutronClient(url, username, password, verbose=verbose)

    try:
        return client.list_agents() if client else None
    
    except Exception, e:
        sys.stderr.write("neutron._getNeutronClient (other exception): " + repr(e) + "\n")
        return None

def networkList(tenant,verbose=0):    
    """
    TODO: Document
    
    :Parameters:
        TODO (string)    Document parameters 
        
    :Returns:
        List of network dictionaries
    :ReturnType:
        list
    """
    url      = 'http://bcsw-os-controller:35357/v2.0'     # TODO make into class/dict and pass in list of projects
    username = 'admin'
    password = 'password'
    project  = tenant.name

    client = _getNeutronClient(url, username, password, project, verbose=verbose)

    try:
        return client.list_networks() if client else None

    except Exception, e:
        sys.stderr.write("neutron.networkList (exception): " + repr(e) + "\n")
        return None
    
def subnetList(tenant, verbose=0):    
    """
    TODO: Document
    
    :Parameters:
        TODO (string)    Document parameters 
        
    :Returns:
        List of network dictionaries
    :ReturnType:
        list
    """
    url      = 'http://bcsw-os-controller:35357/v2.0'     # TODO make into class/dict and pass in list of projects
    username = 'admin'
    password = 'password'
    project  = tenant.name

    client = _getNeutronClient(url, username, password, project, verbose=verbose)

    try:
        return client.list_subnets() if client else None
    
    except Exception, e:
        sys.stderr.write("neutron.subnetList (exception): " + repr(e) + "\n")
        return None

def portList(tenant, verbose=0):    
    """
    TODO: Document
    
    :Parameters:
        TODO (string)    Document parameters 
        
    :Returns:
        List of network dictionaries
    :ReturnType:
        list
    """
    url      = 'http://bcsw-os-controller:35357/v2.0'     # TODO make into class/dict and pass in list of projects
    username = 'admin'
    password = 'password'
    project  = tenant.name

    client = _getNeutronClient(url, username, password, project, verbose=verbose)

    try:
        return client.list_ports() if client else None
    
    except Exception, e:
        sys.stderr.write("neutron.portList (exception): " + repr(e) + "\n")
        return None

def routerList(tenant, verbose=0):    
    """
    TODO: Document
    
    :Parameters:
        TODO (string)    Document parameters 
        
    :Returns:
        List of network dictionaries
    :ReturnType:
        list
    """
    url      = 'http://bcsw-os-controller:35357/v2.0'     # TODO make into class/dict and pass in list of projects
    username = 'admin'
    password = 'password'
    project  = tenant.name

    client = _getNeutronClient(url, username, password, project, verbose=verbose)

    try:
        return client.list_routers() if client else None
    
    except Exception, e:
        sys.stderr.write("neutron.routerList (exception): " + repr(e) + "\n")
        return None
    

def gatewayDeviceList(verbose=0):    
    """
    TODO: Document
    
    :Parameters:
        TODO (string)    Document parameters 
        
    :Returns:
        List of network dictionaries
    :ReturnType:
        list
    """
    url      = 'http://bcsw-os-controller:35357/v2.0'     # TODO make into class/dict and pass in list of projects
    username = 'admin'
    password = 'password'

    client = _getNeutronClient(url, username, password, verbose=verbose)

    try:
        return client.list_gateway_devices() if client else None
    
    except Exception, e:
        sys.stderr.write("neutron.gatewayDeviceList (exception): " + repr(e) + "\n")
        return None


def networkGatewayList(verbose=0):    
    """
    TODO: Document
    
    :Parameters:
        TODO (string)    Document parameters 
        
    :Returns:
        List of network dictionaries
    :ReturnType:
        list
    """
    url      = 'http://bcsw-os-controller:35357/v2.0'     # TODO make into class/dict and pass in list of projects
    username = 'admin'
    password = 'password'

    client = _getNeutronClient(url, username, password, verbose=verbose)

    try:
        return client.list_network_gateways() if client else None

    except Exception, e:
        sys.stderr.write("neutron.networkGatewayList (exception): " + repr(e) + "\n")
        return None
