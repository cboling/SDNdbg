'''
Keystone helpers

@author:    Chip Boling
@copyright: 2015 Boling Consulting Solutions. All rights reserved.
@license:   Artistic License 2.0, http://opensource.org/licenses/Artistic-2.0
@contact:   support@bcsw.net
@deffield   updated: Updated
'''


import sys
import keystoneclient.v2_0.client as ksclient

def _getKeystoneClient(authUrl, username, password, project, region=None, verbose=0):
    """
    Get the neutron client for a particular installation and project
    
    :Parameters:
        TODO (string)    Document parameters 
        
    :Returns:
        client
    :ReturnType:
        keystoneclient
    """

    credentials = { 'username'    : username,
                    'password'    : password,
                    'auth_url'    : authUrl,
                    'tenant_name' : project,
                  }
    if region is not None:
        credentials['region_name'] = region

    try:
        return ksclient.Client(**credentials)

    except ksclient.exceptions, e:
        sys.stderr.write("keystone._getKeystoneClient: " + repr(e) + "\n")

    except Exception, e:
        sys.stderr.write("keystone._getKeystoneClient (other exception): " + repr(e) + "\n")

    return None, "n/a"
            
            
def tenantList(verbose=0):    
    """
    Return a list of tenants dictionaries
    
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
    project  = 'admin'

    client = _getKeystoneClient(url, username, password, project, verbose=verbose)

    return client.tenants.list() if client else None
