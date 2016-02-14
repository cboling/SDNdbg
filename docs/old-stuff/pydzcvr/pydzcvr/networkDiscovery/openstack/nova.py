'''
Python API interface into Nova client

@author:    Chip Boling
@copyright: 2015 Boling Consulting Solutions. All rights reserved.
@license:   Artistic License 2.0, http://opensource.org/licenses/Artistic-2.0
@contact:   support@bcsw.net
@deffield   updated: Updated

@see: http://docs.openstack.org/developer/python-novaclient/api.html
'''

import sys
import novaclient.client as computeClient
#from novaclient import client

# List of nova-client versions supported.  Put in descending order
__novaClientVersions__ = ('3', '2', '1.1', )


def _getNovaClient(authUrl, username, password, project, version=None, verbose=0):
    """
    Get the nova client for a particular installation and project
    
    :Parameters:
        authUrl (string) URL
        
    :Returns:
        (client, apiVersion)
    :ReturnType:
        pair (novaclient, string)
    """
    
    if version is None:
        for ver in __novaClientVersions__:
            try:
                client = computeClient.Client(ver, username, password, project, authUrl)

                if client is not None:
                    return client, ver

            except computeClient.exceptions, e:
                sys.stderr.write("nova._getNovaClient: " + repr(e) + "\n")
                continue

            except Exception, e:
                sys.stderr.write("nova._getNovaClient (other exception): " + repr(e) + "\n")
                continue

        return None, "n/a"
            
    else:
        return (computeClient.Client(version, username, password, project, authUrl), version)

def discoverAll(verbose=0):
    
    # First see if we can get a nova client API interfaces
    
    url      = 'http://bcsw-os-controller:5000'     # TODO make into class and pass in list of projects
    username = 'admin'
    password = 'password'
    project  = 'admin'

    client, apiVersion = _getNovaClient(url, username, password, project, verbose=verbose)
    
    if client:
        print "Found Nova Client with API version %s" % apiVersion
        servers = client.servers.list()
        print "Found %d servers" % servers.count
    else:
        print 'Did not find a valid nova-client API'
    