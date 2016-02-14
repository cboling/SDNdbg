'''


@author:    Chip Boling
@copyright: 2015 Boling Consulting Solutions. All rights reserved.
@license:   Artistic License 2.0, http://opensource.org/licenses/Artistic-2.0
@contact:   support@bcsw.net
@deffield   updated: Updated
'''

def _discoverAllLinks(verbose=0):
    # TODO: Call into any needed APIs
    
    print 'TODO: OVS: Discovery'
    pass
def _discoverAllNodes(verbose=0):
    # TODO: Call into any needed APIs
    
    print 'TODO: OVS: Discovery'
    pass

def discover(verbose=0):
    '''
    Discover all nodes and links in the network that are available through 
    OpenVSwitch/OVSDB APIs
    
    TODO: This will change radically, for now, just do some hardcoded calls
          to various interfaces and see what is available.  Evenutally this
          will be consolidated once patterns emerge.
    '''
    
    # TODO: Figure out what we need to save and how
    _discoverAllNodes(verbose=verbose)
    _discoverAllLinks(verbose=verbose)
    
    pass