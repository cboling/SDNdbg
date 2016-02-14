'''


@author:    Chip Boling
@copyright: 2015 Boling Consulting Solutions. All rights reserved.
@license:   Artistic License 2.0, http://opensource.org/licenses/Artistic-2.0
@contact:   support@bcsw.net
@deffield   updated: Updated
'''

import openstack.discovery as osDisc
import linux.discovery as lnxDisc
import opendaylight.discovery as odlDisc
import openvswitch.discovery as ovsDisc

def discover(verbose=0):
    '''
    Discover all nodes and links in the network

    TODO: This will change radically, for now, just do some hardcoded calls
          to various interfaces and see what is available.  Evenutally this
          will be consolidated once patterns emerge.
          
    TODO: Make each of the discovery calls below optional based on whether or
          not they have the required APIs installed
    '''
    # First search through various APIs and see what we can learn
    
    osDisc.discover(verbose=verbose)
    odlDisc.discover(verbose=verbose)
    ovsDisc.discover(verbose=verbose)
    lnxDisc.discover(verbose=verbose)
    
    return