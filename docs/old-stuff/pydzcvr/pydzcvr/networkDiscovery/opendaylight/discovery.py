'''


@author:  cboling
@copyright:  2015 organization_name. All rights reserved.
@license:    license
@contact:   user_email
@deffield   updated: Updated
'''

def _discoverAllLinks(verbose=0):
    # TODO: Call into any needed APIs
    
    print 'TODO: OVS: Discover Links'
    pass
def _discoverAllNodes(verbose=0):
    # TODO: Call into any needed APIs
    
    print 'TODO: OVS: Discover Nodes'
    pass

def discover(verbose=0):
    '''
    Discover all nodes in the network that are available through 
    OpenDaylight APIs
    
    TODO: This will change radically, for now, just do some hardcoded calls
          to various interfaces and see what is available.  Evenutally this
          will be consolidated once patterns emerge.
    '''
    
    # TODO: Figure out what we need to save and how
    _discoverAllNodes(verbose=verbose)
    _discoverAllLinks(verbose=verbose)
    
    pass